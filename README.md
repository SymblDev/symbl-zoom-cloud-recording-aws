# Symbl Zoom Integration on AWS

The **Zoom Symbl** Integration describes how to ingest or consume Zoom Cloud Recordings prior to sending data into Symbl for processing. The aim is to demonstrate the possibilities of the Symbl API consumption by performing an end-to-end integration to extract meaningful insights. Following that, you'll discover how to consume Zoom Cloud Recordings and get the summary and insights such as topics, questions, and action items, among many other features. This integration not only consumes the recordings but also solves the Symbl concurrency limit. (A default of 50 concurrent async requests)

This integration document should make it easier for consumers to build and deploy the Symbl integration on the cloud. Based on the architecture, the components that are being utilized are part of the **Serverless** Architecture. Hence, it is easy to build and scale things on the cloud. However, there are some known challenges or limitations with this architecture that you will see in the end under the "Limitations" section.

When it comes to building and deploying the components, You’ll see the template file which contains instructions on how to build. These are built using the [Serverless Application Model](https://aws.amazon.com/serverless/sam/) An open-source framework for building serverless applications. Infrastructure as a code approach is what is being followed and that simplifies the end-to-end deployment.

# High Level Architecture

![image](https://user-images.githubusercontent.com/2565797/169448048-69896a9f-dcce-4ec2-be64-3fc2135bfc01.png)

# Prerequisites

* **AWS:**
    * [CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
    * [CLI Config](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)
    * [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
    * [IAM User Policies](https://docs.amazonaws.cn/en_us/IAM/latest/UserGuide/access_policies.html) - Below are the mandatory IAM user policies/permissions that one should have. Please check with your AWS Account Administrator and get the below-mentioned access policies.
        * [AWSCloudFormationFullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAWSCloudFormationFullAccess)
        * [AmazonS3FullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAmazonS3FullAccess)
        * [AmazonSQSFullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAmazonSQSFullAccess)
        * [IAMFullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FIAMFullAccess)
        * [CloudWatchFullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FCloudWatchFullAccess)
        * [AmazonDynamoDBFullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAmazonDynamoDBFullAccess)
        * [AmazonAPIGatewayAdministrator](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAmazonAPIGatewayAdministrator)
        * [AmazonSNSFullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAmazonSNSFullAccess)
        * [AWSCloudFormationFullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAWSCloudFormationFullAccess)
        * [AWSLambda_FullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAWSLambda_FullAccess)
* **Zoom:** 
    * [Zoom developer account](https://marketplace.zoom.us/docs/sdk/native-sdks/developer-accounts) to use zoom APIs
    * [Zoom pre-requirements for enabling cloud recordings for the entire account](https://zoom.us/pricing):
* **Symbl:**  
    * [Registered user account](https://platform.symbl.ai/#/login)
    * [App ID and App Secret](https://docs.symbl.ai/docs/developer-tools/authentication/#step-2-generate-the-access-token) to use Symbl APIs
* **Email:**  
    * Please make sure to [Signup](https://support.google.com/mail/answer/56256?hl=en) a new gmail account for this integration. This is required for sending the summary email to the meeting host.
    * [Allowing less secure apps to access your account](https://support.google.com/accounts/answer/6010255) You’ll have to login and then configure this one for programmatically sending emails from lambda. 
    

# Register an App 

https://marketplace.zoom.us/docs/guides/build/jwt-app/#register-your-app

# Setting up the Source Code 
- Clone or Download the Source Code 
- Use Visual Studio Code or any other editor of your choice to open the source code

# Build the Solution
- On the VS Terminal, Type command **sam build** and press enter key for building the serverless apps  
- On VS Code -> Terminal -> Select New Terminal

<img width="308" alt="Screenshot 2022-04-22 at 12 49 07 PM" 
     src="https://user-images.githubusercontent.com/2565797/165746775-7b7d6df6-8357-4dc1-bbb3-ff9779fa3869.png">

# Deploy the Serverless Application Stack

The “Serverless Application” stack deployment incorporates several components ex: Lambda Layers, S3, SQS, DynamoDB, Lambda Functions etc. required for accomplishing the Zoom Symbl Integration. 

You’ll see how to deploy the serverless application using the **sam deploy** command.

Run with "sam deploy --guided" for the guided deployment

# Configuring the Custom Zoom App Webhook Endpoint

The custom Zoom Application has to be configured with the recording completed webhook endpoint so the integration can receive the necessary “recording completed” event information that can be utilized for processing the recordings.

1. Make sure to login to the [Zoom Developer Account](https://developers.zoom.us/)
2. Navigate to the [Created Apps Section](https://marketplace.zoom.us/user/build)
3. Select the existing app that you wish to configure. 
4. Navigate to the “Feature” section
5. Under the Event Subscription, Click on the **Add Event Subscription**
6. Select the Event Types -> **Recording**
7. Check-mark on the “All Recordings have completed” option

# Configuring the Lambda Environment Variables

This step is dedicated to configuring the lambda environment variables with the AWS Region, App Secret, Zoom JWT Token etc. You’ll learn how to configure them.

Here’s the high-level summary of the lambda function and its environment variables with the description that will help you to understand and update the required aspects of this integration. Up-next, you’ll see a screenshot explaining how to update the environment variables.


<table>
  <tr>
   <td><strong>Lambda Function</strong>
   </td>
   <td><strong>Environment Variable</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td rowspan="2" >CopyZoomRecordingToS3
   </td>
   <td>ZOOM_JWT_TOKEN
   </td>
   <td>Specify your custom zoom app JWT token
   </td>
  </tr>
  <tr>
   <td>SNS_SYMBL_ZOOM_QUEUE
   </td>
   <td>Set with the appropriate Region and Account Id 
<a href="https://sqs.${AWS::Region}.amazonaws.com/${AWS::AccountId}/symbl-zoom">https://sqs.${AWS::Region}.amazonaws.com/${AWS::AccountId}/symbl-zoom</a>
<p>
Alternatively, you can get into the SQS queue named <strong>symbl-zoom</strong> and then copy the ARN
   </td>
  </tr>
  <tr>
   <td rowspan="4" >SubmitZoomRecordingToSymbl
   </td>
   <td>SYMBL_APP_ID
   </td>
   <td>ReplaceWithYourAppId
   </td>
  </tr>
  <tr>
   <td>SYMBL_APP_SECRET
   </td>
   <td>ReplaceWithYourAppSecret
   </td>
  </tr>
  <tr>
   <td>DYNAMO_DB_REGION
   </td>
   <td>Set with the ${AWS::Region} ex: us-east-1
   </td>
  </tr>
  <tr>
   <td>SYMBL_WEBHOOK_URL
   </td>
   <td>ReplaceWithZoomSymblWebhookNotifierApiGatewayUrl
   </td>
  </tr>
  <tr>
   <td>ZoomSymblWebhook
   </td>
   <td>SYMBL_APP_ID
   </td>
   <td>ReplaceWithYourSymblAppId
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>SYMBL_APP_SECRET
   </td>
   <td>ReplaceWithYourAppSecret
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>DYNAMO_DB_REGION
   </td>
   <td>Set with the ${AWS::Region} ex: us-east-1
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>GPASS
   </td>
   <td>ReplaceWithYourGmailPassword
   </td>
  </tr>
</table>

# Running the Application

1. Create a Zoom Meeting
2. If you wish, you may invite participants
3. Make sure to record the meeting
4. End the meeting

Note - 

* Please wait for a couple of minutes so the processing of the recordings can happen. Various factors matter, for example: Number of participants, meeting duration etc.
* If you have configured the “Email” signup and settings as mentioned in the Prerequisite, the meeting host will receive an email consisting of a summary and the meeting insight URL.

# Limitations

1. Please keep in mind about the Zoom Cloud Recording Limits
    1. [Zoom Cloud Recording Limitation](https://support.zoom.us/hc/en-us/articles/203741855-Starting-a-cloud-recording)
    2. [Zoom Cloud Recordings Per Participant](https://community.zoom.com/t5/Meetings/Can-I-record-Zoom-participants-to-separate-audio-files-to-the/td-p/34348)
2. Zoom License Limit. Depending on the license that you have for Zoom, there are restrictions regarding the number of active participants in a given meeting. Here’s an example. Follow the Zoom [Pricing](https://zoom.us/pricing) to get some insights on the Zoom Pricing.
3. The cloud recording(s) processing time varies by the number of audio files and the meeting length. 
That said, there’s a max execution time for lambda. i.e 15 mins. You cannot handle beyond that. In addition to the execution time, there are other constraints like the Max RAM and Storage. It cannot go beyond 10GB. The CopyZoomRecordingToS3 lambda deals with producing the multi-channel stereo audio file and hence, the lambda downloads the cloud recording and then merges the file using FFMPEG. Keep in mind these limits while you test the integration.

# Conclusion

The Zoom Symbl Integration Architecture and its implementation with the “Serverless Architecture” provides you with an idea on how to consume or inject the Zoom Cloud Recordings and process them in an asynchronous manner by merging all the audio recordings and sending it to Symbl using the Async Audio mechanism to extract various intelligence aspects like Topics, Action Items, Follow ups, Summary etc.

If you wish to build a full-scale production ready system for post processing the Zoom Cloud Recordings, It is highly recommended to have a dedicated infrastructure setup for example with EC2 etc. and handle the workflow as stated under the “High Level Architecture” section.


# Troubleshooting

##### How to Rollback the deployment ?

In case of errors, if you are unable to deploy and decide to rollback, please run the following command.

aws cloudformation rollback-stack --stack-name ZoomSymblStack

##### How can I delete a stack?

Please run the following command.

aws cloudformation delete-stack --stack-name ZoomSymblStack

##### Wish to change the default stack name?

Open the file named “**samconfig.toml**” and look for stack_name = "ZoomSymblStack". You may specify the relevant stack name that you wish to use.

##### Unable to deploy the stack due to the capabilities issue?

Open the file named “**samconfig.toml**” and look for the “capabilities”. Please make sure that the capabilities are specified with "CAPABILITY_IAM CAPABILITY_AUTO_EXPAND"

##### How to deal with the Lambda Layer Version mismatch issues?

This integration deals with two Lambda Layers i.e ffmpeg and requests and those were setup as part of the stack. When it comes to the layer version, which is something that is automatically incremented by AWS. Let’s say, if you delete the layer and again try to set it up, the version number will not reset. You’ll see the layer dependency on “**SubmitZoomRecordingToSymbl**” and “**CopyZoomRecordingToS3**”. Please make a note on the Lambda Layer Version and make sure to use that as part of the stack deployment.

##### How can I monitor the Symbl Job status?

Login to AWS and then Search for DynamoDB. You’ll see the below mentioned DynamoDB tables that are being used for processing the recordings.

**zoom_recordings_jobs** is the table that you need to look for. It keeps track of the job_id, conversation_id, meeting_uuid and status.  \
