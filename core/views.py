from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

import requests
from pypdf import PdfReader

from .models import Project, Resource, Summary, Comparison, Tag, ResourceTag
from .forms import RegisterForm, ProjectForm, ResourceForm, ComparisonForm, TagForm



def home(request):
    return render(request, 'core/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})


@login_required
def dashboard(request):
    projects = Project.objects.filter(user=request.user, is_archived=False)
    archived_projects = Project.objects.filter(
    user=request.user,
    is_archived=True
    )

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('dashboard')

    else:
        form = ProjectForm()

    total_projects = projects.count()

    total_resources = Resource.objects.filter(
        project__user=request.user
    ).count()

    total_summaries = Summary.objects.filter(
        resource__project__user=request.user
    ).count()

    total_comparisons = Comparison.objects.filter(
        project__user=request.user
    ).count()

    return render(request, 'core/dashboard.html', {
        'projects': projects,
        'form': form,
        'total_projects': total_projects,
        'total_resources': total_resources,
        'total_summaries': total_summaries,
        'total_comparisons': total_comparisons,
        'archived_projects': archived_projects,
    })


@login_required
def project_detail(request, project_id):

    project = Project.objects.get(
        id=project_id,
        user=request.user
    )

    query = request.GET.get('q', '')

    resources = Resource.objects.filter(
        project=project
    ).prefetch_related('summaries')

    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(authors__icontains=query) |
            Q(abstract_text__icontains=query) |
            Q(resourcetag__tag__name__icontains=query) |
            Q(summaries__summary_text__icontains=query)
        ).distinct()

    comparisons = Comparison.objects.filter(project=project)
    tag_form = TagForm(project=project)

    if request.method == 'POST':

        if 'tag_submit' in request.POST:
            form = ResourceForm()
            comparison_form = ComparisonForm(project=project)
            tag_form = TagForm(request.POST, project=project)

        if tag_form.is_valid():
            resource = tag_form.cleaned_data['resource']
            tag_name = tag_form.cleaned_data['tag_name'].strip().lower()

            tag, created = Tag.objects.get_or_create(name=tag_name)

            ResourceTag.objects.get_or_create(
                resource=resource,
                tag=tag
            )

            return redirect('project_detail', project_id=project.id)

        if 'compare_submit' in request.POST:

            form = ResourceForm()
            comparison_form = ComparisonForm(
                request.POST,
                project=project
            )

            if comparison_form.is_valid():

                resource_one = comparison_form.cleaned_data['resource_one']
                resource_two = comparison_form.cleaned_data['resource_two']

                comparison_text = generate_comparison(
                    resource_one,
                    resource_two
                )

                Comparison.objects.create(
                    project=project,
                    title=f"{resource_one.title} vs {resource_two.title}",
                    description=comparison_text
                )

                return redirect(
                    'project_detail',
                    project_id=project.id
                )

        else:

            form = ResourceForm(
                request.POST,
                request.FILES
            )

            comparison_form = ComparisonForm(project=project)

            if form.is_valid():

                resource = form.save(commit=False)
                resource.project = project
                resource.save()

                return redirect(
                    'project_detail',
                    project_id=project.id
                )

    else:
        form = ResourceForm()
        comparison_form = ComparisonForm(project=project)

    for resource in resources:
        resource.citations = generate_citation(resource)

    return render(request, 'core/project_detail.html', {
        'project': project,
        'resources': resources,
        'form': form,
        'query': query,
        'comparison_form': comparison_form,
        'comparisons': comparisons,
        'tag_form': tag_form,
    })


@login_required
def generate_resource_summary(request, resource_id):

    resource = Resource.objects.get(
        id=resource_id,
        project__user=request.user
    )

    summary_text = generate_summary(resource)

    Summary.objects.create(
        resource=resource,
        summary_text=summary_text,
        citation_text=f"{resource.authors}, {resource.publication_year}",
        key_findings=summary_text
    )

    return redirect(
        'project_detail',
        project_id=resource.project.id
    )

@login_required
def edit_project(request, project_id):

    project = Project.objects.get(
        id=project_id,
        user=request.user
    )

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = ProjectForm(instance=project)

    return render(request, 'core/edit_project.html', {
        'form': form,
        'project': project
    })

@login_required
def delete_project(request, project_id):

    project = Project.objects.get(
        id=project_id,
        user=request.user
    )

    if request.method == 'POST':
        project.is_archived = True
        project.save()
        return redirect('dashboard')

    return render(request, 'core/delete_project.html', {
        'project': project
    })


@login_required
def delete_summary(request, summary_id):

    summary = Summary.objects.get(
        id=summary_id
    )

    project_id = summary.resource.project.id

    summary.delete()

    return redirect(
        'project_detail',
        project_id=project_id
    )

@login_required
def edit_summary(request, summary_id):

    summary = Summary.objects.get(
        id=summary_id,
        resource__project__user=request.user
    )

    if request.method == 'POST':
        summary.summary_text = request.POST.get('summary_text')
        summary.citation_text = request.POST.get('citation_text')
        summary.key_findings = request.POST.get('key_findings')
        summary.save()

        return redirect('project_detail', project_id=summary.resource.project.id)

    return render(request, 'core/edit_summary.html', {
        'summary': summary
    })


@login_required
def edit_resource(request, resource_id):

    resource = Resource.objects.get(
        id=resource_id,
        project__user=request.user
    )

    if request.method == 'POST':
        form = ResourceForm(
            request.POST,
            request.FILES,
            instance=resource
        )

        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=resource.project.id)

    else:
        form = ResourceForm(instance=resource)

    return render(request, 'core/edit_resource.html', {
        'form': form,
        'resource': resource
    })

@login_required
def restore_project(request, project_id):

    project = Project.objects.get(
        id=project_id,
        user=request.user
    )

    project.is_archived = False
    project.save()

    return redirect('dashboard')

@login_required
def delete_resource(request, resource_id):

    resource = Resource.objects.get(
        id=resource_id,
        project__user=request.user
    )

    project_id = resource.project.id

    if resource.file:
        resource.file.delete(save=False)

    resource.delete()

    return redirect(
        'project_detail',
        project_id=project_id
    )

@login_required
def edit_comparison(request, comparison_id):

    comparison = Comparison.objects.get(
        id=comparison_id,
        project__user=request.user
    )

    if request.method == 'POST':
        comparison.title = request.POST.get('title')
        comparison.description = request.POST.get('description')
        comparison.save()

        return redirect('project_detail', project_id=comparison.project.id)

    return render(request, 'core/edit_comparison.html', {
        'comparison': comparison
    })


@login_required
def delete_comparison(request, comparison_id):

    comparison = Comparison.objects.get(
        id=comparison_id,
        project__user=request.user
    )

    project_id = comparison.project.id

    if request.method == 'POST':
        comparison.delete()
        return redirect('project_detail', project_id=project_id)

    return render(request, 'core/delete_comparison.html', {
        'comparison': comparison
    })


def generate_summary(resource):

    text = ""

    if resource.file:

        pdf = PdfReader(resource.file.path)

        for page in pdf.pages[:5]:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    prompt = f"""
    Summarize this research paper in clean simple academic language.

    Rules:
    - Do NOT use markdown
    - Do NOT use ### or **
    - Use short paragraphs
    - Keep it readable for university students

    Include:
    1. Main topic
    2. Key contribution
    3. Important findings
    4. Conclusion

    Paper:
    {text[:4000]}
    """

    headers = {
        "Authorization": f"Bearer {settings.LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-5.4-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()

    print("LLM RESPONSE:", result)

    if "choices" in result:
        return result["choices"][0]["message"]["content"]

    return f"AI summary could not be generated. API response: {result}"


def generate_comparison(resource_one, resource_two):

    text_one = ""
    text_two = ""

    if resource_one.file:

        pdf_one = PdfReader(resource_one.file.path)

        for page in pdf_one.pages[:3]:

            extracted = page.extract_text()

            if extracted:
                text_one += extracted

    if resource_two.file:

        pdf_two = PdfReader(resource_two.file.path)

        for page in pdf_two.pages[:3]:

            extracted = page.extract_text()

            if extracted:
                text_two += extracted

    prompt = f"""
    Compare these two research papers in clean academic language.

    Rules:
    - Do NOT use markdown
    - Do NOT use ### or **
    - Use clear readable paragraphs

    Include:
    1. Main similarity
    2. Main differences
    3. Methodology comparison
    4. Findings comparison
    5. Final conclusion

    Paper 1:
    {text_one[:2500]}

    Paper 2:
    {text_two[:2500]}
    """

    headers = {
        "Authorization": f"Bearer {settings.LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-5.4-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()

    print("COMPARISON RESPONSE:", result)

    if "choices" in result:
        return result["choices"][0]["message"]["content"]

    return f"AI comparison could not be generated. API response: {result}"


def generate_citation(resource):

    authors = resource.authors or "Unknown Author"
    year = resource.publication_year or "n.d."
    title = resource.title

    apa = f"{authors} ({year}). {title}."

    ieee = f"[1] {authors}, \"{title},\" {year}."

    return {
        "apa": apa,
        "ieee": ieee
    }

@login_required
def export_project_pdf(request, project_id):

    project = Project.objects.get(
        id=project_id,
        user=request.user
    )

    resources = Resource.objects.filter(project=project).prefetch_related(
        'summaries',
        'resourcetag_set__tag'
    )

    comparisons = Comparison.objects.filter(project=project)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{project.title}_report.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, f"ResearchDoc Project Report")
    y -= 30

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, f"Project: {project.title}")
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Description: {project.description}")
    y -= 35

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Resources")
    y -= 25

    for resource in resources:

        if y < 100:
            pdf.showPage()
            y = height - 50

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, f"- {resource.title}")
        y -= 18

        pdf.setFont("Helvetica", 10)
        pdf.drawString(70, y, f"Type: {resource.resource_type}")
        y -= 15

        tags = ", ".join([
            rt.tag.name for rt in resource.resourcetag_set.all()
        ]) or "No tags"

        pdf.drawString(70, y, f"Tags: {tags}")
        y -= 15

        citation = generate_citation(resource)
        pdf.drawString(70, y, f"APA: {citation['apa'][:90]}")
        y -= 15
        pdf.drawString(70, y, f"IEEE: {citation['ieee'][:90]}")
        y -= 25

        for summary in resource.summaries.all():

            if y < 140:
                pdf.showPage()
                y = height - 50

            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(70, y, "AI Summary:")
            y -= 15

            pdf.setFont("Helvetica", 9)

            summary_text = (
                summary.summary_text
                .replace("\n", " ")
                .replace("■", "")
                .replace("•", "-")
            )[:900]

            for line in [summary_text[i:i+95] for i in range(0, len(summary_text), 95)]:
                if y < 80:
                    pdf.showPage()
                    y = height - 50

                pdf.drawString(90, y, line)
                y -= 12

            y -= 15

    if comparisons:
        if y < 120:
            pdf.showPage()
            y = height - 50

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "AI Comparisons")
        y -= 25

        for comparison in comparisons:

            if y < 120:
                pdf.showPage()
                y = height - 50

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, y, comparison.title)
            y -= 18

            pdf.setFont("Helvetica", 9)
            text = (
                comparison.description
                .replace("\n", " ")
                .replace("■", "")
                .replace("•", "-")
            )[:900]

            for line in [text[i:i+95] for i in range(0, len(text), 95)]:
                if y < 80:
                    pdf.showPage()
                    y = height - 50

                pdf.drawString(70, y, line)
                y -= 12

            y -= 15

    pdf.save()

    return response