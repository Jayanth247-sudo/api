from flask import Flask, request, jsonify
from jobspy import scrape_jobs

app = Flask(__name__)

# Route to scrape jobs
@app.route('/scrape-jobs', methods=['GET'])
def get_jobs():
    # Get parameters from the request URL
    site_name = request.args.get('site_name', 'linkedin')
    search_term = request.args.get('search_term', 'software engineer')
    location = request.args.get('location', 'New York, NY')
    results_wanted = int(request.args.get('results_wanted', 20))
    hours_old = int(request.args.get('hours_old', 72))
    
    # Add linkedin_fetch_description parameter
    linkedin_fetch_description = request.args.get('linkedin_fetch_description', 'false').lower() == 'true'
    
    # Scrape jobs based on parameters
    jobs = scrape_jobs(
        site_name=[site_name],
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
        linkedin_fetch_description=linkedin_fetch_description  # Add this parameter
    )
    
    # Convert jobs to a list of dictionaries for easy JSON response
    jobs_list = jobs.to_dict('records')
    
    # Remove null values from the response
    for job in jobs_list:
        job_clean = {k: v for k, v in job.items() if v is not None}
        job.clear()
        job.update(job_clean)
    return jsonify(jobs_list)

if __name__ == '__main__':
    app.run(debug=True)
