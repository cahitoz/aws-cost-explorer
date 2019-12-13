# aws-cost-explorer

This PYTHON script retrieves all COST items allocated to an account. If the account is the root account of and Organization then all cost of sub/child accounts is also retrieved.

Below are the cost items that are retrieved.

[ACCOUNTNO]   AWS Directory Service                    39.0198646426   USD     True<br>
[ACCOUNTNO]   AWS Key Management Service                           0   USD     True<br>
[ACCOUNTNO]   Amazon DynamoDB                           0.0000000402   USD     True<br>
[ACCOUNTNO]   EC2 - Other                              53.2571615722   USD     True<br>
[ACCOUNTNO]   Amazon Elastic Compute Cloud - Compute   88.7085999866   USD     True<br>
[ACCOUNTNO]   Amazon Simple Storage Service             0.0007794019   USD     True<br>
[ACCOUNTNO]   Amazon WorkSpaces                        46.9499999976   USD     True<br>
[ACCOUNTNO]   AmazonCloudWatch                                     0   USD     True<br>
[ACCOUNTNO]   Tax                                              43.31   USD     True

To use this, you need to install aws-cli on the calling account.


