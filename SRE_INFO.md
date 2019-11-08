# SRE Info
This is the SRE_INFO.md file which should be found in the root of any source code that is
administered by the Mozilla IT SRE team. We are available on #it-sre on slack.

## Infra Access
To access the itsre-apps EKS cluster, first use aws-vault to gain access to the account. Once you're authenticated,
you can run
```
aws eks update-kubeconfig --name k8s-apps-prod-us-west-2
```

[SRE aws-vault setup](https://mana.mozilla.org/wiki/display/SRE/aws-vault)

[SRE account guide](https://mana.mozilla.org/wiki/display/SRE/AWS+Account+access+guide)

[SRE AWS accounts](https://github.com/mozilla-it/itsre-accounts/blob/master/accounts/mozilla-itsre/terraform.tfvars#L5)

## Secrets
This uses bitnami sealed secrets

## Source Repos
[air.mozilla.org](https://github.com/mozilla-it/air.mozilla.org)

## Monitoring
New Relic Synthetics checks

## SSL Certificates
ACM

## Cloud Account
AWS account 783633885093

