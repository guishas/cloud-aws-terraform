# Cloud Project - Automating AWS Infrastructure with Terraform (IaaC)

Python CLI for creating AWS Infrastructure with Terraform

## Requirements

- Python 3.8+ (https://www.python.org/downloads)
- Terraform (https://developer.hashicorp.com/terraform/downloads)

## How to run the project

First, clone to project to your desired folder

<pre><code> git clone https://github.com/guishas/cloud-aws-terraform.git</code></pre>

Then, install the dependencies needed to run the project at the root folder

<pre><code>pip install -r requirements.txt</code></pre>

If you want, export your AWS credentials to the environment (it's optional) by typing in the console:

<pre><code> 
export AWS_ACCESS_KEY_ID="<YOUR_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<YOUR_SECRET_ACCESS_KEY>"
</code></pre>

After, run the CLI by typing in the console:

<pre><code>python cli.py</code></pre>
