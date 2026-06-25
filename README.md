# ICAI Exam Results Clone - Project Summary

This project is a high-fidelity clone of the official ICAI (Institute of Chartered Accountants of India) Examination Results web portal, deployed to a custom domain with a mock result verification system.

## 🔗 Live Site
* **URL**: [https://www.icainic.org](https://www.icainic.org)
* **Custom Domain Hosting**: Vercel
* **SSL Status**: Fully Active (Secure HTTPS)

---

## 📋 Project Specifications & Work Completed

1. **Homepage Reconstruction (`index.html`)**:
   * Cloned the exact visual design of the official landing page at `https://caresults.icai.org/caresult/`.
   * Updated result and merit list links to point to the local credential verification page.
   * Tailored CSS for mobile responsiveness using a custom `@media` viewport wrapper to keep the header elements properly scaled and centered on mobile viewports.

2. **Result Verification Page (`intermediate-group-2.html`)**:
   * Cloned the official results checking form.
   * Integrated a custom JavaScript checker in `window.onload` to validate inputted credentials entirely client-side.
   * If correct credentials are submitted, it dynamically replaces the page container with a perfectly styled, responsive scorecard matching the official ICAI markup layout.

3. **Official Asset Integration**:
   * Extracted the high-resolution base64 logo from the official ICAI website and saved it locally to `images/moblogo.png` to keep files lightweight and ensure correct display dimensions (81x80).
   * Captured the official captcha image and stored it locally as `captcha.png`.

---

## 🔑 Verification & Login Details

To view the mock scorecard on the live website:

1. Go to the homepage: [https://www.icainic.org](https://www.icainic.org)
2. Click on **Intermediate Examination** or **Intermediate Examination - UNITS**.
3. Input the following exact credentials:
   * **Roll No.**: `661841`
   * **Registration No.**: `CR00725489` *(Case-sensitive)*
   * **Security Code (Captcha)**: `b27d4q`
4. Click **Submit**.

### Scorecard Contents (Mohit Jangid)
* **Candidate Name**: MOHIT JANGID
* **Roll Number**: 661841
* **Group II Result**: Successful
  * **Cost and Management Accounting**: 062
  * **Auditing and Ethics**: 048
  * **Financial Management and Strategic Management**: 050
  * **Total**: 160

---

## 📁 File Structure

```text
icai/
├── index.html                   # Main results landing page (cloned from caresults.icai.org)
├── intermediate-group-2.html    # Credential entry form & dynamic scorecard generator
├── captcha.png                  # Captcha code graphic ("b27d4q")
├── README.md                    # Project summary and documentation (this file)
├── images/
│   ├── moblogo.png              # Official high-resolution ICAI logo
│   └── ...                      # Other landing page static assets
├── css/                         # Cloned stylesheets
├── js/                          # Cloned helper scripts
└── bootstrap/                   # Bootstrap framework styles & layout files
```

---

## ⚙️ Deployment & Domain DNS Settings

The website is hosted on **Vercel** and connected to the custom domain **icainic.org**.

### DNS Records Configuration
To point the custom domain to the Vercel hosting platform, the following records were set in the domain registrar's DNS panel (Network Solutions):

| Record Type | Host / Name | Value | Purpose |
| :--- | :--- | :--- | :--- |
| **A** | `@` (Root) | `76.76.21.21` (or equivalent Vercel IP) | Resolves `icainic.org` |
| **CNAME** | `www` | `cname.vercel-dns.com` | Resolves `www.icainic.org` |

*Vercel automatically provisions and renews the SSL certificates once the above DNS records propagate.*
