import requests
import urllib.parse
from lxml import html
from .config import config

class FileReader:
    def readFile(self):
        s=requests.Session()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # ------------ 1 ---------------------
        payload='LoginFormData.UserName=' + urllib.parse.quote(config["IE"]["UserName"])  + '&LoginFormData.Password=' + urllib.parse.quote(config["IE"]["Password"])
        response = s.request("POST", config["IE"]["URL"], headers=headers, data=payload)

        tree = html.fromstring(response.text)
        div = tree.xpath('//p[@data-testid="account-card-account-number" and text()="' + config["IE"]["AccountId"] + '"]/../../..')[0]
        selectedAccountNumber = div.xpath('.//input[@name="SelectedAccount.AccountNumber"]')[0].value
        rvt = div.xpath('.//input[@name="rvt"]')[0].value
        flowFormId = div.xpath('.//input[@name="flow-form-id"]')[0].value
        flowHandler = div.xpath('.//input[@name="FlowHandler"]')[0].value
        flowScreenName = div.xpath('.//input[@name="FlowScreenName"]')[0].value

        # ------------ 2 ---------------------
        payloadOnEvent = 'SelectedAccount.AccountNumber=' + selectedAccountNumber + '&triggers_event=AccountSelection.ToAccountAndMeterDetails&rvt=' + rvt + '&flow-form-id=' + flowFormId + '&FlowHandler=' + flowHandler + '&FlowScreenName=' + flowScreenName
        responseOnEvent = s.request("POST", config["IE"]["URL"] + "/Accounts/OnEvent", headers=headers, data=payloadOnEvent)
        treeAccount = html.fromstring(responseOnEvent.text)
        accountLink = treeAccount.xpath('//a[@data-testid="nav-details-link"]/@href')[0]

        # -------------- 3 --------------------
        accountContent = s.get(config["IE"]["URL"] + accountLink)
        treeDownload = html.fromstring(accountContent.text)
        downloadLink = treeDownload.xpath('//a[@data-testid="details-consumption-data-download"]/@href')[0]


        # -------------- 4 --------------------
        downloadContent = s.get(config["IE"]["URL"] + downloadLink)
        return downloadContent.content.decode("utf-8")