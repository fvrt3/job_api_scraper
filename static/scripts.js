let currentPage = 1;

async function loadJobs(page) {
    currentPage = page;
    const keyword = document.getElementById('keyword').value;
    const location = document.getElementById('location').value;
    const minSalary = document.getElementById('minSalary').value;
    const maxSalary = document.getElementById('maxSalary').value;

    const params = new URLSearchParams({
        page,
        limit: 10
    });
    if (keyword) params.append('keyword', keyword);
    if (location) params.append('location', location);
    if (minSalary) params.append('min_salary', minSalary);
    if (maxSalary) params.append('max_salary', maxSalary);

    const res = await fetch(`/jobs?${params.toString()}`);
    const data = await res.json();
    renderJobs(data.results);
    document.getElementById('pageInfo').innerText = `Page ${data.page}`;
}

function renderJobs(jobs) {
    const container = document.getElementById('jobs');
    container.innerHTML = '';
    if (!jobs.length) {
        container.innerHTML = '<center><p>No jobs matched your preferences. Try adjusting the filters to see more results.</p></center>';
        return;
    }
    jobs.forEach(job => {
        const div = document.createElement('div');
        div.className = 'job-card';
        div.innerHTML = `
            <div class="job-title">${job.title}</div>
            <div><strong>Company:</strong> ${job.company}</div>
            <div><strong>Location:</strong> ${job.location}</div>
            <div><strong>Salary:</strong> ${job.salary || 'N/A'}</div>
            <span class="toggle-description" onclick="this.parentElement.classList.toggle('expanded')">
                ${job.description ? 'Show Description' : 'No Description'}
            </span>
            <div class="job-description">${job.description || ''}</div>
            <div><a href="${job.url}" target="_blank">View Job</a></div>
        `;
        container.appendChild(div);
    });
}

function nextPage() {
    loadJobs(currentPage + 1);
}

function prevPage() {
    if (currentPage > 1) {
        loadJobs(currentPage - 1);
    }
}

loadJobs(1);