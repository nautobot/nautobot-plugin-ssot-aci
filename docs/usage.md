## Usage
You use the plugin by navigating to **Plugins > Dashboard** in Nautobot.  Then click on **Cisco ACI Data Source**.
![Nautobot SSoT Dashboard](https://user-images.githubusercontent.com/6945229/155611179-8d39b79b-8c35-4a74-a871-2ebbc36a2b94.png)
 
From the **Cisco ACI Data Source** page you can click **Sync Now** to begin a synchronization job and view the history of synchronization jobs.

![SSoT ACI Dashboard](https://user-images.githubusercontent.com/6945229/155611423-ad0381f0-7877-491f-b5ac-fb725f9c8150.png)

After clicking **Sync Now**, you can select whether you would like to do a dry-run as well as schedule when you would like the job to run.  With a dry-run, you can see what information will be brought from ACI into Nautobot without actually performing the synchronization. The job can be run immediately, scheduled to run at a later date/time, or configured to run hourly, daily, or weekly at a specified date/time. 

![SSoT ACI Job Options](https://user-images.githubusercontent.com/6945229/155612395-afca143d-1805-414b-a3c6-9f59566ba46a.png)

Once you click **Run Job Now**, you will see the logs as the job progresses. When synchronization completes, you can click the **SSoT Sync Details** button to view the changes, or proposed changes, to Nautobot records.   

![SSoT ACI Job Post-Run](https://user-images.githubusercontent.com/6945229/155612666-5488e5a3-92cb-44f1-af9b-83a6cb55b379.png)

![SSoT ACI Job Sync Details](https://user-images.githubusercontent.com/6945229/155613017-74163984-ba88-4cb3-a1ce-0fd2430a75ee.png)