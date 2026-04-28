# BehaveBDDPlaywrightAI

    A **BDD test automation framework (Python)** that combines **Behave**, **API**, 
    **Playwright* and **Generative AI** (Claude Code) to deliver intelligent,
    self-healing and visually-aware end-to-end testing.


## Project Structure

```text
BehaveBDDPlaywrightAI/                                                                                                                                                                                                                                                           
  ├── .gitignore                                                                                                                                                                                                                                                                   
  ├── CLAUDE.md                                                                                                                                                                                                                                                                    
  ├── readme.md                                                                                                                                                                                                                                                                    
  ├── requirements.txt                                                                                                                                                                                                                                                             
  ├── run_regression_publish.bat                                                                                                                                                                                                                                                   
  ├── send_report.py                                                                                                                                                                                                                                                               
  ├── current_log_path.txt
  │
  ├── ConfigurationData/
  │   └── conf.ini
  │
  ├── Utilities/
  │   ├── allure_report_helper.py
  │   ├── configReader.py
  │   ├── email_sender.py
  │   ├── image_compare.py
  │   └── logUtil.py
  │
  ├── ai/
  │   ├── genAI_gemini.py
  │   ├── mcp_client.py
  │   ├── mcp_tools.py
  │   └── openAIAgentTest.py
  │
  ├── features/
  │   ├── environment.py
  │   ├── registration.feature
  │   ├── visualTesting.feature
  │   ├── ai.feature
  │   │
  │   ├── steps/
  │   │   ├── ai_step.py
  │   │   ├── registration_step.py
  │   │   └── visualTesting_step.py
  │   │
  │   ├── pageobjects/
  │   │   ├── BasePage.py
  │   │   └── RegistrationPage.py
  │   │
  │   └── apitests/
  │       └── test_playwright_API.py
  │
  ├── Downloads/
  │   └── Selenium.jar
  │
  ├── visual_actual/
  │   └── homepage.png
  │
  ├── visual_baseline/
  │   └── homepage.png
  │
  └── visual_diff/
```    

<br><br>
✅ CI/CD Execution Evidence
Below is real execution evidence of the framework running successfully in a Jenkins Continuous Integration (CI) environment.
This confirms that the automation framework is CI-ready, stable, and fully integrated with Jenkins.

<img width="1416" height="471" alt="image" src="https://github.com/user-attachments/assets/650e4cc1-6f04-4b19-8119-be6cfcc94c49" />
