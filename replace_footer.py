
import os
import re

def update_footers():
    base_dir = r"p:\AI-website-clone\node_site\public"
    
    # New Footer HTML content
    new_footer = """
  <footer>
    <div class="container-fluid">
      <div class="row">
        <!-- Column 1: Institution -->
        <div class="col-lg-3 col-md-6 mb-4">
          <div class="ft-logo">
            <h3 class="titel32 w700 mb-1" style="color:#E85626 !important">
              Symbiosis Artificial<br>
              Intelligence Institute
            </h3>
          </div>
          <hr style="margin: 15px 0; border-color: #ddd;">
          <p style="font-size: 15px; line-height: 1.6; color: #555;">
            Symbiosis Artificial Intelligence Institute (SAII), Constituent of SYMBIOSIS INTERNATIONAL (DEEMED UNIVERSITY).
          </p>
        </div>

        <!-- Column 2: Quick Links -->
        <div class="col-lg-3 col-md-6 mb-4">
          <h4 class="footer-title">Quick Links</h4>
          <ul class="footer-links">
            <li><a href="index.html">Home</a></li>
            <li><a href="about-us.html">About Us</a></li>
            <li><a href="programs.html">Opportunities & Resources</a></li>
            <li><a href="contact-us.html">Contact Us</a></li>
          </ul>
        </div>

        <!-- Column 3: Address -->
        <div class="col-lg-3 col-md-6 mb-4">
          <h4 class="footer-title">Address</h4>
          <p class="footer-address">
            Room No: 18219<br>
            Ground floor<br>
            KMC Administrative block<br>
            KMC, Manipal<br>
            Madhav Nagar – 576104
          </p>
        </div>

        <!-- Column 4: Contact -->
        <div class="col-lg-3 col-md-6 mb-4">
          <h4 class="footer-title">Contact</h4>
          <div class="footer-contact">
             <p>
               <i class="fa fa-envelope" style="color:#E85626; margin-right:8px;"></i>
               <a href="mailto:aihealthcare.kmc@manipal.edu">aihealthcare.kmc@manipal.edu</a>
             </p>
          </div>
          <div class="footer-social">
            <a href="https://www.linkedin.com/school/symbiosis-artificial-intelligence-institute-saii-%E0%A4%B8%E0%A4%BE%E0%A4%88" target="_blank"><i class="fa fa-linkedin"></i></a>
            <a href="https://www.instagram.com/symbiosis_saii/" target="_blank"><i class="fa fa-instagram"></i></a>
            <a href="https://www.youtube.com/@SymbiosisSaiiPune" target="_blank"><i class="fa fa-youtube-play"></i></a>
            <a href="https://x.com/SAII_Symbiosis" target="_blank"><i class="fa fa-twitter"></i></a>
            <a href="https://www.facebook.com/saii.pune/" target="_blank"><i class="fa fa-facebook"></i></a>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Preserved Floating Button -->
    <a class="apply-steps-btn video-hub" href="video-hub.html" target="_blank">
      <img alt="Video Icon" src="/assets/images/video-icon-removebg-preview.png"
        style="width:37px; height:auto; margin-bottom:-8px; vertical-align:middle;" />
      What's Next
    </a>
  </footer>
"""

    # Regex to capture footer block
    # Matches <footer ... > ... </footer>
    # Note: re.DOTALL is crucial
    footer_pattern = re.compile(r'<footer\b[^>]*>(.*?)</footer>', re.DOTALL | re.IGNORECASE)

    print("--- Replacing Footers ---")
    
    count = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                fpath = os.path.join(root, file)
                
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    continue
                
                # Check if footer exists
                if '<footer' in content:
                    new_content = re.sub(footer_pattern, new_footer.strip(), content)
                    
                    if new_content != content:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated {file}")
                        count += 1
                    else:
                        print(f"No match in {file} (regex failed?)")
                else:
                    print(f"No footer in {file}")

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    update_footers()
