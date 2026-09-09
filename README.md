SocEng-Project — Phishing Awareness Campaign

An authorized social engineering and phishing-awareness project developed for the Macomb College Vulnerability Analysis Report.

The project demonstrates how publicly available information can be used to create realistic, targeted phishing-awareness scenarios. The campaign focused on OSINT (Open-Source Intelligence), email design, target identification, and social-engineering awareness.

Project Overview

The goal of this project was to demonstrate how an attacker could use publicly available information to create a convincing, targeted phishing email.

The project consisted of:

Conducting OSINT research on publicly available information
Identifying appropriate campaign targets within the authorized scope
Creating realistic HTML-based email content
Designing custom email header and footer banners
Creating multiple phishing-themed email templates
Manually composing emails using the prepared HTML content
Sending the simulated phishing emails to the identified targets
Documenting the campaign methodology and results

The campaign was conducted as an authorized academic security exercise.

Project Files
File	Purpose
README.md	Project documentation
email_template.html	Main phishing-awareness email template
email_template_maintenance.html	Maintenance-themed email template
email_template_survey.html	Survey-themed email template
header_banner.jpg	Custom email header graphic
footer_banner.jpg	Custom email footer graphic
requirements.txt	Project dependencies
vercel.json	Deployment configuration
api/	Supporting project components
Note

The project did not use the targets.csv, targets.json, send_log.csv, or click_log.csv workflow described in earlier documentation. Targets were identified through OSINT, and the emails were manually created and sent using the prepared HTML content.

OSINT Methodology

The first stage of the project involved gathering information from publicly available sources.

The objective was to identify information that could potentially be used to make a phishing email appear more legitimate or relevant to its recipient.

The research process included:

Identifying publicly available information sources.
Searching for information about individuals and organizational roles within the approved scope.
Correlating publicly available information to identify potential targets.
Recording relevant information needed to construct the awareness scenario.
Using the collected information to make the simulated emails more realistic.

Only information available through authorized, publicly accessible sources was used.

Email Development

Custom HTML email content was developed for the campaign.

The project included multiple scenarios, including:

Maintenance Notification

A simulated maintenance-related communication designed to demonstrate how routine IT or organizational notifications can be used as a social-engineering lure.

Survey

A simulated survey-related communication demonstrating how requests for feedback or participation can be used to encourage recipients to interact with an email.

Custom Email Branding

The email templates were designed with custom:

Header banners
Footer banners
HTML formatting
Email layouts
Organizational-style visual elements

The HTML content was then copied into the email body when preparing the campaign messages.

Campaign Process

The overall workflow was:

Public Information
       ↓
      OSINT
       ↓
Target Identification
       ↓
Scenario Development
       ↓
HTML Email Design
       ↓
Header / Footer Creation
       ↓
Manual Email Preparation
       ↓
Authorized Campaign
       ↓
Results & Analysis
Security Awareness Objective

The purpose of the campaign was not simply to send deceptive emails. The larger objective was to demonstrate the social-engineering techniques that can make phishing messages convincing.

The project demonstrates several common phishing concepts:

Personalization
Authority impersonation
Familiar organizational branding
Urgency
Routine maintenance notifications
Survey requests
Use of publicly available information
Professional-looking HTML formatting

Understanding these techniques can help organizations and employees recognize suspicious communications before interacting with them.

Ethical Considerations

This project was conducted as part of an authorized academic cybersecurity exercise.

The following principles applied to the campaign:

Targets were limited to the approved scope.
OSINT information was obtained from publicly available sources.
The campaign was conducted for educational and security-awareness purposes.
No malware was distributed.
No unauthorized account access was attempted.
Credentials were not intentionally collected.
Information obtained during the exercise was handled as assessment data.
Campaign activity was documented for inclusion in the final assessment.

If sensitive credentials or other sensitive information were unexpectedly disclosed during the exercise, the appropriate instructor/project supervisor would be notified immediately.

Technologies & Techniques

Technologies:

HTML
Python
GitHub
Email
Web-based OSINT resources

Security techniques:

Open-Source Intelligence (OSINT)
Social engineering
Phishing simulation
Target profiling
Email analysis
Security awareness testing
Academic Context

This project was developed as part of the Macomb College Vulnerability Analysis Report and was intended to demonstrate the risks associated with targeted social-engineering attacks.

The project highlights an important security principle:

A phishing attack does not necessarily require sophisticated malware or technical exploitation. Publicly available information combined with convincing communication can be enough to create a credible social-engineering scenario.

Disclaimer

This project is intended for authorized educational, security-awareness, and cybersecurity assessment purposes only.

Any use of the techniques or materials described in this repository against individuals, organizations, or systems without appropriate authorization is prohibited.
