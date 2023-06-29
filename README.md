# Udacity Cloud DevOps using Microsoft Azure Nanodegree Program Project 3: Ensuring Quality Releases

## Table of Contents
* [Introduction](#Introduction)
* [Getting Started](#Getting-Started)
* [Install our dependencies](#Install-our-dependencies)
* [Configure storage account and state backend for Terraform](#Configure-storage-account-and-state-backend-for-Terraform)
* [Create a Service Principal for Terraform](#Create-a-Service-Principal-for-Terraform)
* [Configure Pipeline Environment](#Configure-Pipeline-Environment)
* [Create Postman Test Suites](#Create-Postman-Test-Suites)
* [Create a Selenium test for a website](#Create-a-Selenium-test-for-a-website)
* [Create a Test Suite with JMeter](#Create-a-Test-Suite-with-JMeter)
* [Enable Monitoring & Observability](#Enable-Monitoring-&-Observability)
  * [Azure Monitor](#Azure-Monitor)
  * [Azure Log Analytics](#Azure-Log-Analytics)
* [Conclusion](#Conclusion)
* [Future Work](#Future-Work)
* [References](#References)

## Introduction
This is the third project for the Udacity Cloud DevOps using Microsoft Azure Nanodegree Program, where we create disposable test environments and run a variety of automated tests with the click of a button. Additionally, we monitor and provide insight into an application's behavior, and determine root causes by querying the application’s custom log files.

For this project we use the following tools:

- Azure DevOps: For creating a CI/CD pipeline to run Terraform scripts and execute tests with Selenium, Postman and Jmeter
- Terraform: For creating Azure infrastructure as code (IaS)
- Postman: For creating a regression test suite and publish the results to Azure Pipelines.
- Selenium: For creating a UI test suite for a website.
- JMeter: For creating a Stress Test Suite and an Endurance Test Suite.
- Azure Monitor: For configuring alerts to trigger given a condition from an App Service.

To visualize the project this overview can help:

<img width="443" alt="project-overview-capture" src="https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/74fa1b03-7d06-42e6-b1a7-c0ac8c99c3a6">



## Getting Started
Due to using a Udacity Cloud Lab a Service Principal is already given.
For this project we will perform the following steps:
1. Install our dependencies
2. Configure storage account and state backend for Terraform
4. Configure Pipeline Environment
5. Create Postman Test Suites
6. Create a Selenium test for a website
7. Create a Test Suite with JMeter
8. Enable Monitoring & Observability

## Install our dependencies
For the successful run of this project we need to do the following steps:
1. Install Visual Studio Code: https://code.visualstudio.com/
2. Create an Outlook Account: https://outlook.live.com/
3. Create a free Azure Account: https://azure.microsoft.com/
4. Create an Azure Devops account: https://azure.microsoft.com/services/devops/
5. Install Azure CLI: https://docs.microsoft.com/cli/azure/install-azure-cli?view=azure-cli-latest
6. Install Terraform: https://learn.hashicorp.com/tutorials/terraform/install-cli#install-terraform
7. Install the Java Development Kit: https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html
8. Install JMeter: https://jmeter.apache.org/download_jmeter.cgi
9. Install Postman: https://www.postman.com/downloads/
10. Install Python: https://www.python.org/downloads/
11. Install Selenium for Python: https://pypi.org/project/selenium/
12. Install Chromedriver: https://sites.google.com/a/chromium.org/chromedriver/downloads

## Configure storage account and state backend for Terraform
Terraform state is used to reconcile deployed resources with Terraform configurations. State allows Terraform to know what Azure resources to add, update, or delete. 
For the project we will use Azure Storage for persisting the Terraform state in remote storage. For this we will run the ```terraformconfig.sh``` file, which has the necessary configuration for creating a blob storage to store the state.

We jump into the terraform folder and run the script:

cd Udacity_Azure_Devops_Project_03/terraform
chmod +x terraformconfig.sh
./terraformconfig.sh

We will get 3 outputs:
- storage_account_name
- container_name 
- access_key

We will use these variables and put it into the following file:
terraform/environments/test/main.tf

```
terraform {
  backend "azurerm" {
    storage_account_name = ""
    container_name       = ""
    key                  = ""
    access_key           = ""
  }
}
```
We are now ready to configure an Azure DevOps Pipeline.

## Configure Azure Pipelines
We will need to install Terraform extension from Microsoft DevLabs to use terraform in our DevOps Project, install it (after having created the project)
by going to Organization Settings/General/Extensions/Browse Marketplace and click on terraform extension icon.

Now we need to create a new Service Connection in the Project by going to Project Settings -> Service connections -> New service connection -> Azure Resource Manager -> Service Principal (Automated). Name the new service connection to Azure Resource Manager as ```myServiceConnection```.
This service connection will be used in the ```azure-pipelines.yml``` file.

The next step is to upload our ```terraform.tvars``` to Azure Devops as a Secure File, to do this we have to navigate to Pipelines -> Library -> Secure Files -> + Secure File -> Upload File. Now the file should be uploaded.

Further ahead when the pipeline is created, remember to go into the "Pipeline permissions" menu by clicking in the file name in the "Secure Files" menu and add the pipeline that we will be using.

We are ready to run the Provision stage of our pipeline.

If all the configuration was correct, then the terraform apply command should be successful, and our resources should be deployed to the cloud.

![Terraform_Apply](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/111d9492-6f8c-4dd6-b33f-58d93548eec5)


## Configure Pipeline Environment
After Terraform deploys the VM in Azure we need to manually register the Virtual Machine in Pipelines -> Environments -> TEST -> Add resource -> Virtual Machines -> Linux. Then copy the registration script and manually log into the virtual machine (via SSH), paste it in and run the script.

![Create_Environment](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/6ba93d39-cdef-48ef-a67c-512bc09b4b87)

![Configure_Environment](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/f918fd80-a4d2-40b1-9f9c-024584f37d1e)

This enables Azure Pipelines to run commands in that Virtual Machine. 


## Create Postman Test Suites
For this part we will use Postman and Newman to test each endpoint of the web app available in the ```fakerestapi``` folder. We will use Postman to test the endpoints, and when we are done we will download their definitions in .json and then use them in our project to run them using Newman in the Azure Pipeline.

We created both regression tests and validation tests, and an environment to store our variables. Also, we defined the publishing of test results to Test Plans of Azure Devops.

Please note, that the API that we are testing (http://dummy.restapiexample.com) is quite unstable as it recieves a lot of traffic, so some calls to the endpoints might fail with an error code and test results may vary according to the time of usage.

After we run the Postman tests in our pipeline we can get Test Results in Test Plans -> Runs -> Postman Test Results. We get the following result in the Run Summary page:

![Postman_Test_Results_01](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/d9ab9f70-6b19-49dd-bdba-3c5ff952974f)

![Postman_Test_Results_02](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/966476e7-e04e-4734-99b8-d7e99dae1b63)

![Postman_Test_Results_03](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/17eb6f08-bb71-4912-a8ba-588c7535eee8)


In the Pipeline run we can check the logs of the publishing of the test results.

![Postman_Publishing](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/5b2cc7ea-5c77-492f-b695-d1647ebec745)


## Create a Selenium test for a website
For this part of the project we will use selenium-test.py file and run it in a "headless" mode.

We included the website https://www.saucedemo.com/ in order to test login, adding 6 items to cart and removing those 6 items afterwards.

In the Azure Pipeline Job section we can check the logs of the Selenium Test.

![Selenium_Test_Result](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/3b8a9e29-3914-435a-af6e-e31e890ada44)

We also defined an artifact that contains the logs for all Selenium runs.

![Selenium_Publishing](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/115d5423-ff50-4d07-a530-2cc77045e036)


## Create a Test Suite with JMeter
In this step we will create both endurance tests and stress tests with Apache JMeter.

When running the tests in Azure Pipelines we can get summaries for both of them.

![JMeter_EnduranceTest_Result](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/061f5c54-1482-43c3-a857-4fd138f1681c)


![JMeter_StressTest_Result](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/b04dda46-1e1c-4033-9f2d-ae13360b9bb7)


## Enable Monitoring & Observability

In this section, we will enable Monitoring & Observability in our Virtual Machine and App Service to observe the effects of our tests.

### Azure Monitor
We can set up alerts to fire when a resource meets certain conditions. For example, we will set up an email to fire when requests are more or equal than 1 or 10, respectively.

In the Azure Portal choose an AppService, go to Monitoring and click on Alert, then click + New Rule.

In Condition we will select ```Requests (Platform)```, in Alert logic we will select for Operator ```Greater than or equal to``` and Threshold value as 1 or 10, respectively. Leave the rest of the configuration as it is.

In Actions we will add an action group, then create an action group named ```myActGroup```. In Notification we will select for Notification Type ```Email/SMS message/Push/Voice.``` and add our email and finally create it. 

 After adding Alert Rule Details you can hit ```Create Alert Rule```.

The Alert Rules should look as follows:

![Create_Alert_Rule](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/e3d85994-0c49-4865-8bda-0588e11ff067)

When the alert is activated/fired, we get an email, which is posted here in 3 parts: 

![Alert_Email_Part_1](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/93619bbb-c87a-4c55-a7a4-5657e3412122)
![Alert_Email_Part_2](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/16eb8c37-d098-4412-ae22-2a4b0f8d8b1b)
![Alert_Email_Part_3](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/b9bc4a92-805b-473a-a3ed-8b73f457bb65)


We can also look at the requests graph available in the Azure Portal:

![Web_App_HTTP_404_Metrics](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/b1b733a7-0959-41f2-bd3c-91d2d7118f13)


### Azure Log Analytics

Log Analytics is a tool in the Azure portal that's used to edit and run log queries against data in the Azure Monitor Logs store.
Using this tool, we can check in the Azure Portal for example the AppSercvice HTTP-Logs.

![Query_Web_App_HTTP_Log_Results_02](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/a9c6ae51-a5d5-4d39-a667-616e5a123e27)

![Query_Web_App_HTTP_Log_Diagram](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/66e6d626-dec3-431d-a18a-7a2f3ba248a5)

Besides, we can also check the output of the Selenium Test Suite. For this we will configure custom logs.

To configure custom logs you have to go to your Log Analytics Workspace -> Settings -> Custom logs -> Upload sample file.

We will download selenium-test.log, that we generated earlier in the pipeline. It looks like this:

2023-06-29 07:43:08 - Starting the browser...
2023-06-29 07:43:14 - Browser started successfully.
2023-06-29 07:43:14 - Login
2023-06-29 07:43:14 - Navigating to the demo page to login.
2023-06-29 07:43:16 - Login with username standard_user and password secret_sauce successful
2023-06-29 07:43:16 - Add items
2023-06-29 07:43:16 - Add all items to the cart
2023-06-29 07:43:16 - Added Sauce Labs Backpack
2023-06-29 07:43:17 - Added Sauce Labs Bike Light
2023-06-29 07:43:17 - Added Sauce Labs Bolt T-Shirt
2023-06-29 07:43:17 - Added Sauce Labs Fleece Jacket
2023-06-29 07:43:17 - Added Sauce Labs Onesie
2023-06-29 07:43:17 - Added Test.allTheThings() T-Shirt (Red)
2023-06-29 07:43:18 - Finished testing adding items to the cart
2023-06-29 07:43:18 - Remove items
2023-06-29 07:43:18 - Number of items in the cart = 6
2023-06-29 07:43:18 - Removed Sauce Labs Backpack
2023-06-29 07:43:18 - Removed Sauce Labs Bike Light
2023-06-29 07:43:18 - Removed Sauce Labs Bolt T-Shirt
2023-06-29 07:43:19 - Removed Sauce Labs Fleece Jacket
2023-06-29 07:43:19 - Removed Sauce Labs Onesie
2023-06-29 07:43:19 - Removed Test.allTheThings() T-Shirt (Red)
2023-06-29 07:43:19 - Finshed testing removing items from the cart
2023-06-29 07:43:19 - Tests Completed
2023-06-29 09:13:56 - Starting the browser...
2023-06-29 09:14:00 - Browser started successfully.
2023-06-29 09:14:00 - Login
2023-06-29 09:14:00 - Navigating to the demo page to login.
2023-06-29 09:14:03 - Login with username standard_user and password secret_sauce successful
2023-06-29 09:14:03 - Add items
2023-06-29 09:14:03 - Add all items to the cart
2023-06-29 09:14:03 - Added Sauce Labs Backpack
2023-06-29 09:14:03 - Added Sauce Labs Bike Light
2023-06-29 09:14:03 - Added Sauce Labs Bolt T-Shirt
2023-06-29 09:14:03 - Added Sauce Labs Fleece Jacket
2023-06-29 09:14:03 - Added Sauce Labs Onesie
2023-06-29 09:14:03 - Added Test.allTheThings() T-Shirt (Red)
2023-06-29 09:14:04 - Finished testing adding items to the cart
2023-06-29 09:14:04 - Remove items
2023-06-29 09:14:04 - Number of items in the cart = 6
2023-06-29 09:14:04 - Removed Sauce Labs Backpack
2023-06-29 09:14:04 - Removed Sauce Labs Bike Light
2023-06-29 09:14:04 - Removed Sauce Labs Bolt T-Shirt
2023-06-29 09:14:04 - Removed Sauce Labs Fleece Jacket
2023-06-29 09:14:04 - Removed Sauce Labs Onesie
2023-06-29 09:14:04 - Removed Test.allTheThings() T-Shirt (Red)
2023-06-29 09:14:04 - Finshed testing removing items from the cart
2023-06-29 09:14:04 - Tests Completed
2023-06-29 09:30:37 - Starting the browser...
2023-06-29 09:30:38 - Browser started successfully.
2023-06-29 09:30:38 - Login
2023-06-29 09:30:38 - Navigating to the demo page to login.
2023-06-29 09:30:39 - Login with username standard_user and password secret_sauce successful
2023-06-29 09:30:39 - Add items
2023-06-29 09:30:39 - Add all items to the cart
2023-06-29 09:30:39 - Added Sauce Labs Backpack
2023-06-29 09:30:39 - Added Sauce Labs Bike Light
2023-06-29 09:30:39 - Added Sauce Labs Bolt T-Shirt
2023-06-29 09:30:39 - Added Sauce Labs Fleece Jacket
2023-06-29 09:30:39 - Added Sauce Labs Onesie
2023-06-29 09:30:39 - Added Test.allTheThings() T-Shirt (Red)
2023-06-29 09:30:40 - Finished testing adding items to the cart
2023-06-29 09:30:40 - Remove items
2023-06-29 09:30:40 - Number of items in the cart = 6
2023-06-29 09:30:40 - Removed Sauce Labs Backpack
2023-06-29 09:30:40 - Removed Sauce Labs Bike Light
2023-06-29 09:30:40 - Removed Sauce Labs Bolt T-Shirt
2023-06-29 09:30:40 - Removed Sauce Labs Fleece Jacket
2023-06-29 09:30:40 - Removed Sauce Labs Onesie
2023-06-29 09:30:40 - Removed Test.allTheThings() T-Shirt (Red)
2023-06-29 09:30:40 - Finshed testing removing items from the cart
2023-06-29 09:30:40 - Tests Completed

In Record delimiter we will select New line.

In Collection paths we will select Linux and set the path where the logs are located on the VM, in our case /home/devopsagent/myagent/azagent/_work/1/s/log/selenium/selenium-test.log

In Details, we will define the Custom log name as SeleniumTestLogs and afterwards we create it:

![Custom_Table_Log_Analytics](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/ee8d6458-6d99-46db-b9f4-d2d190ef232d)

We can query it in the Logs section of Log Analytics Workspace by writing SeleniumTestLogs_CL:

## Conclusion
Finally, we can see, that our complete pipeline has been succesfully executed!

![Pipeline_Result](https://github.com/brem02/Udacity_Azure_Devops_Project_03/assets/122722304/71729cf3-750e-4971-9c26-dd43bb050340)

## Future Work
- We could cause errors or other scenarios for the AppService/VM and demonstrate these behaviors in the test suites as well as in Azure Monitor and Log Analytics.

## References
- [Udacity Project Starter Files](https://video.udacity-data.com/topher/2020/June/5ed815bf_project-starter-resources/project-starter-resources.zip)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Outlook](https://outlook.live.com/)
- [Azure](https://azure.microsoft.com/)
- [Azure DevOps](https://azure.microsoft.com/services/devops/)
- [Azure Command Line Interface](https://docs.microsoft.com/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli#install-terraform)
- [Terraform Azure Documentation](https://learn.hashicorp.com/collections/terraform/azure-get-started)
- [Java Development Kit](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html)
- [Jmeter](https://jmeter.apache.org/download_jmeter.cgi)
- [Postman](https://www.postman.com/downloads/)
- [Python](https://www.python.org/downloads/)
- [Selenium for Python](https://pypi.org/project/selenium/)
- [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- [Tutorial: Store Terraform state in Azure Storage](https://docs.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage)
- [Terraform - Microsoft DevLabs](https://marketplace.visualstudio.com/items?itemName=ms-devlabs.custom-terraform-tasks)
- [Resources in YAML](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/resources?view=azure-devops&tabs=schema)
- [Terraform on Azure Pipelines Best Practices](https://julie.io/writing/terraform-on-azure-pipelines-best-practices/)
- [Use secure files](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/secure-files?view=azure-devops)
- [Sauce Demo](https://www.saucedemo.com/)
- [Running collections on the command line with Newman](https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/)
- [Dummy Rest API Example](http://dummy.restapiexample.com)
