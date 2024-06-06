# Web Scraping Project

## Overview
This project is a general-purpose web scraping tool designed to extract data from dynamic web pages. It uses Selenium for browser automation, BeautifulSoup for parsing HTML content, and httpx + asyncio for making asynchronous HTTP requests. The extracted data is then cleaned, transformed into a CSV file, and uploaded to an AWS S3 bucket.

## Features
- **Headless Browser Automation**: Utilizes headless Chrome via Selenium for scraping.
- **Asynchronous Requests**: Leverages asyncio and httpx for efficient data fetching.
- **Data Parsing**: Employs BeautifulSoup and lxml for parsing and extracting data.
- **AWS S3 Integration**: Includes functionality to upload the resulting dataset to an AWS S3 bucket.

## Prerequisites
- Python 3.11
- Docker
- AWS Account (for S3 bucket access)

## Installation
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Build the Docker image using the provided Dockerfile.


## Handle AWS credinitials
For handling AWS credentials, it’s important not to hardcode them into your Dockerfile or image. Instead, use one of the following methods:
- **Environment Variables**: Pass your AWS credentials as environment variables when you run the Docker container:

  ```docker run -e AWS_ACCESS_KEY_ID=your_access_key_id -e AWS_SECRET_ACCESS_KEY=your_secret_access_key my-python-app```

  **Note:** Replace ```your_access_key_id``` and ```your_secret_access_key``` with your actual AWS credentials.
- **IAM Roles**: If you’re running the container on an AWS EC2 instance, you can assign an IAM role to the instance with the necessary permissions, and the AWS SDK will automatically use these credentials.
- **Docker Secrets**: If you’re using Docker Swarm, you can use Docker secrets to securely transmit your AWS credentials to the container.
- **Bind Mounts**: You can also mount your local .aws credentials directory to the Docker container:

  ```docker run -v ~/.aws:/root/.aws:ro my-python-app```

  Remember to replace my-python-app with the actual name of your Docker image. Also, ensure that your application code is configured to use boto3 to interact with AWS services, utilizing the   
  credentials provided through one of these methods.

## Building your Docker image
For building and running your Docker image, you would use commands like:

```
docker build -t my-python-app .
docker run my-python-app
```

**Note:** Make sure to replace ```my-python-app``` with the name you want for your Docker image.


## Automation
The script can be automated using cron jobs to run at specified intervals. This ensures that the container runs the script periodically to scrape and update the data.
**Note**: This involves changing you dockerfile to run the ```cron.sh``` file instead of the Python script.

## Configuration
Before running the script, ensure to set the following variables in the ```script.py```:
- ```landing_page_URL```: The URL of the web page to start scraping from.
- ```extend_page_button```: The CSS selector for the ‘Load More’ button (if applicable).
- ```css_selector_of_the_products_list```:  The CSS selector for the list containing the products.
- ```bucket_name```:  The name of your AWS S3 bucket.
- ```s3_file_name```: The desired name for your file in the S3 bucket.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.


# Credits
Special thanks to the people who helped me making this possible!

**Peter Faso**: https://www.linkedin.com/in/peterfaso/

**Imad Klailat**: https://github.com/klailatimad

**Mohammed Alghizzi**: https://www.linkedin.com/in/mohammedalghizzi/

**Khalid Sharahili**: https://github.com/kaledhub
