$("#cat-1").owlCarousel({
    items: 33,
    loop: !0,
    margin: 15,
    nav: !1,
    dots: !1,
    autoplay: !0,
    slideTransition: "linear",
    autoplayTimeout: 2e3,
    autoplaySpeed: 2e3,
    responsive: { 0: { items: 2 }, 600: { items: 3 }, 1e3: { items: 3 } },
}),
    $("#cat-2").owlCarousel({
        items: 3,
        loop: !0,
        margin: 15,
        nav: !1,
        dots: !1,
        autoplay: !0,
        slideTransition: "linear",
        autoplayTimeout: 2e3,
        autoplaySpeed: 2e3,
        rtl: !0,
        responsive: { 0: { items: 2 }, 600: { items: 3 }, 1e3: { items: 3 } },
    }),
    $("#cat-3").owlCarousel({
        items: 4,
        loop: !0,
        margin: 20,
        nav: !0,
        dots: !1,
        autoplay: !0,
        autoplayTimeout: 2e3,
        autoplaySpeed: 2e3,
        responsive: { 0: { items: 1 }, 600: { items: 3 }, 1e3: { items: 4 } },
    }),
    $("#cat-4").owlCarousel({
        items: 4,
        loop: !0,
        margin: 20,
        nav: !0,
        dots: !1,
        autoplay: !0,
        autoplayTimeout: 2e3,
        autoplaySpeed: 2e3,
        responsive: { 0: { items: 1 }, 600: { items: 3 }, 1e3: { items: 4 } },
    }),
    $("#cat-5").owlCarousel({
        items: 4,
        loop: !0,
        margin: 20,
        nav: !0,
        dots: !1,
        autoplay: !0,
        autoplayTimeout: 2e3,
        autoplaySpeed: 2e3,
        responsive: { 0: { items: 1 }, 600: { items: 3 }, 1e3: { items: 4 } },
    }),
    $("#cat-6").owlCarousel({
        items: 4,
        loop: !1,
        margin: 20,
        nav: !0,
        dots: !1,
        autoplay: !1,
        autoplayTimeout: 2e3,
        autoplaySpeed: 2e3,
        responsive: { 0: { items: 1 }, 600: { items: 3 }, 1e3: { items: 4 } },
    }),
    $("#cat-7").owlCarousel({
        items: 33,
        loop: !0,
        margin: 15,
        nav: !1,
        dots: !1,
        autoplay: !0,
        slideTransition: "linear",
        autoplayTimeout: 2e3,
        autoplaySpeed: 2e3,
        responsive: { 0: { items: 2 }, 600: { items: 3 }, 1e3: { items: 3 } },
    }),
    $("#cat-8").owlCarousel({
        items: 3,
        loop: !0,
        margin: 15,
        nav: !1,
        dots: !1,
        autoplay: !0,
        slideTransition: "linear",
        autoplayTimeout: 2e3,
        autoplaySpeed: 2e3,
        rtl: !0,
        responsive: { 0: { items: 2 }, 600: { items: 3 }, 1e3: { items: 3 } },
    }),
    $("#cat-9").owlCarousel({
        items: 1,
        loop: !0,
        margin: 20,
        nav: !0,
        autoplay: !1,
    });

// 3D Horizontal Coverflow Logic
const cfSlides = document.querySelectorAll('.about-coverflow .coverflow-slide');
if (cfSlides.length > 0) {
    let cfIdx = 2; // Center start (0-4 => 2)
    const cfCount = cfSlides.length;
    let cfTimer;

    function renderCoverflow() {
        cfSlides.forEach((slide, i) => {
            slide.className = 'coverflow-slide'; // Reset

            // Calculate wrapped distance from active index
            let d = (i - cfIdx);
            while (d <= -3) d += cfCount;
            while (d > 2) d -= cfCount;

            // Assign classes based on distance
            if (d === 0) slide.classList.add('active');
            else if (d === -1) slide.classList.add('left');
            else if (d === 1) slide.classList.add('right');
            else if (d === -2) slide.classList.add('left-hide');
            else if (d === 2) slide.classList.add('right-hide');
            // Any other distance (shouldn't happen with 5 items) is hidden by default CSS
        });
    }

    function autoCoverflow() {
        cfIdx = (cfIdx + 1) % cfCount;
        renderCoverflow();
    }

    // Init
    renderCoverflow();

    // Auto-Play
    cfTimer = setInterval(autoCoverflow, 3000);

    // Hover Pause
    const cfContainer = document.querySelector('.about-coverflow-wrapper');
    if (cfContainer) {
        cfContainer.addEventListener('mouseenter', () => clearInterval(cfTimer));
        cfContainer.addEventListener('mouseleave', () => cfTimer = setInterval(autoCoverflow, 3000));
    }
}





document.addEventListener('DOMContentLoaded', function () {
    // UTM Script

    const params = new URLSearchParams(window.location.search);

    // Exit if no UTM params
    if (![...params.keys()].some(k => k.startsWith('utm_'))) return;

    const links = document.querySelectorAll('a');

    links.forEach(link => {
        const href = link.getAttribute('href');

        // Skip empty or anchor links
        if (!href || href.startsWith('#')) return;

        try {
            const url = new URL(href, window.location.origin);

            // Append ONLY UTM params
            params.forEach((value, key) => {
                if (key.startsWith('utm_')) {
                    url.searchParams.set(key, value);
                }
            });

            link.href = url.toString();

        } catch (e) {
            console.warn('Invalid URL skipped:', href);
        }
    });
});





// ======================================================
// Global "Connect With Us" Form & Modal Logic
// ======================================================

document.addEventListener("DOMContentLoaded", function () {

    // ------------------------------------------------------
    // EnquiryModalController: Strict Singleton & State Management
    // ------------------------------------------------------
    const EnquiryModalController = {
        isOpen: false,
        isAnimating: false,
        modalId: 'globalEnquiryModal',
        triggerClasses: ['open-enquiry-modal', 'apply-now-btn'],
        closeTimer: null,

        init: function () {
            // 1. Singleton Guard
            if (window.enquiryModalInitialized) return;
            window.enquiryModalInitialized = true;

            console.log("EnquiryModalController: Initializing...");

            // 2. Aggressive DOM Cleanup (Remove duplicates/legacy)
            this.forceCleanupDOM();

            // 3. Inject Single Source of Truth
            this.injectModal();

            // 4. Bind Events (Delegation)
            this.bindEvents();
        },

        forceCleanupDOM: function () {
            const existing = document.querySelectorAll('#globalEnquiryModal, .enquiry-modal-overlay');
            if (existing.length > 0) {
                console.warn("EnquiryModalController: Cleaning up " + existing.length + " stale modals.");
                existing.forEach(el => el.remove());
            }
        },

        injectModal: function () {
            const formHTML = `
            <div class="connect-form-wrapper" style="padding: 2.5rem; background: #fff; font-family: 'Montserrat', sans-serif;">
                <div class="form-header text-center mb-4">
                    <h2 style="color: #000; font-weight: 700; font-size: 1.8rem; margin-bottom: 0.5rem;" class="form-title">Welcome!</h2>
                    <p style="color: #666; font-size: 0.95rem; margin-bottom: 0;">Kindly provide your details for further communication</p>
                </div>
                
                <form id="globalEnquiryForm" novalidate>
                   <!-- Email -->
                    <div class="mb-3 input-group">
                        <span class="input-group-text bg-white border-end-0" style="border-radius: 6px 0 0 6px; border-color: #ced4da; min-width: 45px;"><i class="fa fa-envelope-o" style="color: #999;"></i></span>
                        <input type="email" class="form-control border-start-0" name="email" placeholder="Email address*" required style="height: 45px; border-radius: 0 6px 6px 0; border-color: #ced4da; box-shadow: none;">
                        <div class="invalid-feedback">Please enter a valid email.</div>
                    </div>

                    <!-- Phone -->
                    <div class="mb-3 input-group">
                        <span class="input-group-text border-end-0" style="background: #f8f9fa; border-color: #ced4da; border-radius: 6px 0 0 6px; color: #333; font-weight: 600; font-size: 14px; min-width: 50px; justify-content: center;">+91</span>
                        <input type="tel" class="form-control border-start-0" name="phone" placeholder="Phone number" pattern="[0-9]*" inputmode="numeric" style="height: 45px; border-radius: 0 6px 6px 0; border-color: #ced4da; border-left: 1px solid #dee2e6;">
                    </div>

                    <!-- Company -->
                    <div class="mb-3 input-group">
                        <span class="input-group-text bg-white border-end-0" style="border-radius: 6px 0 0 6px; border-color: #ced4da; min-width: 45px;"><i class="fa fa-home" style="color: #999; font-size: 16px;"></i></span>
                         <input type="text" class="form-control border-start-0" name="company" placeholder="Company / Organization name*" required style="height: 45px; border-radius: 0 6px 6px 0; border-color: #ced4da; box-shadow: none;">
                        <div class="invalid-feedback">Company name is required.</div>
                    </div>

                    <!-- Collaboration Type -->
                    <div class="mb-3 position-relative">
                        <select class="form-select" name="collaboration_type" required style="height: 45px; border-radius: 6px; border-color: #ced4da;">
                            <option value="" selected disabled>Collaboration type*</option>
                            <option value="Academic">Academic</option>
                            <option value="Research">Research</option>
                            <option value="Innovation">Innovation</option>
                            <option value="Project">Project</option>
                        </select>
                        <div class="invalid-feedback">Please select a type.</div>
                    </div>

                    <!-- Message -->
                    <div class="mb-4">
                        <textarea class="form-control" name="message" rows="4" placeholder="Comments / message*" required style="border-radius: 6px; border-color: #ced4da; resize: vertical; padding: 12px;"></textarea>
                        <div class="invalid-feedback">Message is required.</div>
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" id="eq-submit-btn" class="btn w-100" style="background-color: #E85626; color: white; height: 50px; border-radius: 6px; font-weight: 600; border: none;">Submit Inquiry</button>
                    
                    <!-- Status Messages -->
                    <div id="eq-success-msg" style="display: none; margin-top: 15px; padding: 10px; border-radius: 6px; background-color: #e8f5e9; color: #2e7d32; border: 1px solid #c8e6c9; text-align: center;">
                        <i class="fa fa-check-circle me-1"></i> Inquiry submitted successfully.
                    </div>
                    <div id="eq-error-msg" style="display: none; margin-top: 15px; padding: 10px; border-radius: 6px; background-color: #ffebee; color: #c62828; border: 1px solid #ffcdd2; text-align: center;">
                        Submission failed. Please try again.
                    </div>
                </form>
            </div>`;

            const modalLayout = `
            <div id="${this.modalId}" class="enquiry-modal-overlay">
                <div class="enquiry-modal-box">
                    <button class="enquiry-modal-close" aria-label="Close form">&times;</button>
                    <div class="enquiry-modal-content">
                        ${formHTML}
                    </div>
                </div>
            </div>
            <style>
                .enquiry-modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(5px); z-index: 99999; display: none; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s ease; }
                .enquiry-modal-overlay.active { display: flex; opacity: 1; }
                .enquiry-modal-overlay:not(.active) { pointer-events: none; }
                .enquiry-modal-box { background: #fff; width: 95%; max-width: 520px; max-height: 90vh; position: relative; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); overflow-y: auto; transform: scale(0.95); transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); padding-top: 10px; }
                .enquiry-modal-overlay.active .enquiry-modal-box { transform: scale(1); }
                .enquiry-modal-close { position: absolute; top: 15px; right: 20px; background: transparent; border: none; font-size: 30px; line-height: 1; cursor: pointer; color: #888; z-index: 10001; transition: color 0.2s; }
                .enquiry-modal-close:hover { color: #E85626; }
                .was-validated .form-control:invalid, .was-validated .form-select:invalid { border-color: #dc3545 !important; background-image: none !important; }
                .form-control:focus, .form-select:focus { border-color: #E85626 !important; box-shadow: 0 0 0 0.2rem rgba(232, 86, 38, 0.2) !important; outline: none; }
            </style>`;

            document.body.insertAdjacentHTML('beforeend', modalLayout);

            // Also inject into Contact Us page container if it exists
            const contactContainer = document.getElementById('contactPageFormContainer');
            if (contactContainer) {
                contactContainer.innerHTML = formHTML;
                this.setupForm(contactContainer.querySelector('form'));
            }

            // Setup Modal Form
            const modal = document.getElementById(this.modalId);
            if (modal) {
                this.setupForm(modal.querySelector('form'));
            }
        },

        bindEvents: function () {
            // Global Trigger Delegation
            document.addEventListener('click', (e) => {
                const target = e.target.closest('a, button, [data-open]');

                // 1. Open Trigger
                if (target && this.isTrigger(target)) {
                    this.handleOpen(e, target);
                    return;
                }

                // 2. Close Trigger (X or Backdrop)
                if (e.target.closest('.enquiry-modal-close') || e.target.classList.contains('enquiry-modal-overlay')) {
                    e.preventDefault();
                    this.close();
                }
            });

            // ESC Key
            document.addEventListener('keydown', (e) => {
                if (e.key === "Escape" && this.isOpen) this.close();
            });
        },

        isTrigger: function (el) {
            // Check Class List
            if (this.triggerClasses.some(cls => el.classList.contains(cls))) return true;
            // Check Data Attribute
            if (el.dataset.open === 'enquiry-modal') return true;
            return false;
        },

        handleOpen: function (e, el) {
            e.preventDefault();
            e.stopPropagation();
            if (this.isOpen) return;
            this.open();
        },

        open: function () {
            this.isOpen = true;
            const modal = document.getElementById(this.modalId);
            if (!modal) return;

            // Reset state
            this.resetModalState(modal);

            // Show
            modal.style.display = 'flex';
            // Force reflow
            void modal.offsetWidth;

            modal.classList.add('active');
            modal.style.pointerEvents = 'auto';
            document.body.style.overflow = 'hidden';

            console.log("EnquiryModalController: Opened.");
        },

        close: function () {
            const modal = document.getElementById(this.modalId);
            if (!modal) return;

            this.isOpen = false;

            // Immediate Lock
            modal.style.pointerEvents = 'none';
            document.body.style.overflow = '';
            modal.classList.remove('active');

            // Cleanup Timer
            if (this.closeTimer) clearTimeout(this.closeTimer);
            this.closeTimer = setTimeout(() => {
                modal.style.display = 'none';
                this.resetModalState(modal); // Final internal cleanup
            }, 300);

            console.log("EnquiryModalController: Closed.");
        },

        resetModalState: function (modal) {
            // Reset form inside modal
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
                form.classList.remove('was-validated');
                form.style.display = 'block';
                const successMsg = form.querySelector('#eq-success-msg');
                if (successMsg) successMsg.style.display = 'none';
                const errorMsg = form.querySelector('#eq-error-msg');
                if (errorMsg) errorMsg.style.display = 'none';
            }
        },

        setupForm: function (form) {
            if (!form || form.dataset.ready) return;
            form.dataset.ready = "true";

            // Input Validation Logic
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('blur', () => form.classList.add('was-validated'));
                if (input.name === 'phone') {
                    input.addEventListener('input', (e) => e.target.value = e.target.value.replace(/[^0-9]/g, ''));
                }
            });

            form.addEventListener('submit', (e) => {
                e.preventDefault();
                e.stopPropagation();

                if (!form.checkValidity()) {
                    form.classList.add('was-validated');
                    return;
                }

                // Submitting...
                const btn = form.querySelector('button[type="submit"]');
                const origText = btn.innerText;
                btn.disabled = true;
                btn.innerText = "Sending...";

                // Simulate
                setTimeout(() => {
                    btn.disabled = false;
                    btn.innerText = origText;
                    form.style.display = 'none';
                    const success = form.querySelector('#eq-success-msg');
                    if (success) success.style.display = 'block';

                    // If in modal, auto-close
                    if (form.closest('#globalEnquiryModal')) {
                        setTimeout(() => this.close(), 2000);
                    }
                }, 1000);
            });
        }
    };

    // Run
    EnquiryModalController.init();
});


// ======================================================
// Active Navbar Link Auto-highlight
// ======================================================
document.addEventListener('DOMContentLoaded', function () {
    // 1. Get the current path, normalize. Default to 'index.html' if root.
    let currentPath = window.location.pathname;
    if (currentPath === '/' || currentPath === '') {
        currentPath = '/index.html';
    }

    // Select all nav links and dropdown items
    const navItems = document.querySelectorAll('.navbar-nav .nav-link, .navbar-nav .dropdown-item');

    navItems.forEach(item => {
        const href = item.getAttribute('href');

        // Ensure href exists and isn't just a hash
        if (!href || href === '#') return;

        // 2. See if the currentPath ends with the href (useful for nested paths vs root items)
        // or matches it exactly.
        // We use endswith because href might be 'about-us.html' but absolute is '/about-us.html'
        if (currentPath.endsWith(href)) {
            // Give this item the active class
            item.classList.add('active');

            // 3. If it's a dropdown-item, we also want to light up its parent dropdown-toggle
            if (item.classList.contains('dropdown-item')) {
                const parentDropdown = item.closest('.nav-item.dropdown, .dropend');
                if (parentDropdown) {
                    const toggle = parentDropdown.querySelector('.dropdown-toggle');
                    if (toggle) {
                        toggle.classList.add('active');

                        // If it's a nested dropdown (dropend), also light up the top level nav-link
                        if (parentDropdown.classList.contains('dropend')) {
                            const topLevelContainer = parentDropdown.closest('.nav-item.dropdown');
                            if (topLevelContainer) {
                                const topToggle = topLevelContainer.querySelector('.nav-link.dropdown-toggle');
                                if (topToggle) topToggle.classList.add('active');
                            }
                        }
                    }
                }
            }
        }
    });
});
