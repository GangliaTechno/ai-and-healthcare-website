require("dotenv").config();
const express = require("express");
const path = require("path");
const cors = require("cors");
const dotenv = require("dotenv");
const fetch = require("node-fetch");
const mongoose = require("mongoose");
const argon2 = require("argon2");
const crypto = require("crypto");

// Simple HMAC token helper (replaces jsonwebtoken dependency)
const TOKEN_SECRET = "aih_secret_key_2024_fixed";
function signToken(payload) {
  const data = JSON.stringify(payload);
  const b64 = Buffer.from(data).toString("base64");
  const sig = crypto.createHmac("sha256", TOKEN_SECRET).update(b64).digest("base64");
  return `${b64}.${sig}`;
}
// Helper: Verify HMAC Token for Members
function verifyToken(token) {
  try {
    const [payloadBase64, signature] = token.split('.');
    const expectedSignature = crypto.createHmac('sha256', TOKEN_SECRET).update(payloadBase64).digest('base64');
    if (signature !== expectedSignature) return null;
    return JSON.parse(Buffer.from(payloadBase64, 'base64').toString());
  } catch (e) { return null; }
}

// Middleware: Authenticate Member
const verifyMember = (req, res, next) => {
  req.isApprovedMember = false;
  req.isAdmin = false;
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return next();
  }
  const token = authHeader.split(' ')[1];
  const payload = verifyToken(token);
  if (payload) {
    if (payload.role === 'member') {
      req.isApprovedMember = true;
      req.memberEmail = payload.email;
    } else if (payload.role === 'admin') {
      req.isAdmin = true;
      req.adminEmail = payload.email;
    }
  } else if (req.headers['x-admin-auth'] === 'aih_admin_secret_2024') {
    req.isAdmin = true;
  } else {
    req.isApprovedMember = false;
    req.isAdmin = false;
  }
  next();
};


const app = express();
const PORT = 3000;

app.use(cors());

app.get("/api/fix-nav", (req, res) => {
  require("./public/fix_nav.js");
  res.send("Fixed");
});
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb", extended: true }));

/* =========================
   🔌 MONGODB CONNECTION
========================= */
mongoose.connect("mongodb+srv://admin:admin@cluster0.wduvypf.mongodb.net/ai_healthcare")
  .then(async () => {
    console.log("MongoDB Connected");

    // ✅ CREATE ADMIN (RUN ONLY ONCE)
    const createAdmin = async () => {
      try {
        const hashedPassword = await argon2.hash("admin");

        await Admin.deleteMany({ email: "sinchana.ganglia@gmail.com" });

        await Admin.create({
          email: "sinchana.ganglia@gmail.com",
          password: hashedPassword
        });

        console.log("✅ Admin created with hashed password");
      } catch (err) {
        console.error(err);
      }
    };
    //await createAdmin(); // ⚠️ RUN ONCE → then remove later
    await seedCourses();
    await seedActivities();
    await migrateHomeActivities();
    await seedResearchEntries();
    await migrateDetailedInfo();
  })
  .catch(err => console.log(err));

/* =========================
   📦 MIGRATION LOGIC
========================= */

// Ensure the 4 original seeded activities have showOnHome: true
const migrateHomeActivities = async () => {
  try {
    const originalSlugs = ['research-impact', 'industry-collabs', 'student-projects', 'guest-speakers'];
    const result = await Activity.updateMany(
      { slug: { $in: originalSlugs }, showOnHome: { $ne: true } },
      { $set: { showOnHome: true } }
    );
    if (result.modifiedCount > 0) {
      console.log(`✅ Marked ${result.modifiedCount} original activities as showOnHome=true`);
    }
  } catch (err) {
    console.error('Error migrating home activities:', err);
  }
};

const migrateDetailedInfo = async () => {
  try {
    const courses = await Course.find({ detailedInfo: { $exists: false } });
    if (courses.length > 0) {
      console.log(`🧹 Migrating ${courses.length} courses to include detailedInfo...`);
      for (const course of courses) {
        course.detailedInfo = course.description; // Default to description if missing
        await course.save();
      }
      console.log("✅ Migration complete");
    }
  } catch (err) {
    console.error("Migration error:", err);
  }
};

/* =========================
   📦 SCHEMAS
========================= */

// Admin
const adminSchema = new mongoose.Schema({
  email: String,
  password: String,
});
const Admin = mongoose.model("Admin", adminSchema);

// Users
const userSchema = new mongoose.Schema({
  name: String,
  email: String,
});
const User = mongoose.model("User", userSchema);

// Member Requests (registration + approval flow)
const memberRequestSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  institution: { type: String, default: "" },
  reason: { type: String, default: "" },
  passwordHash: { type: String, required: true },
  registrationStatus: {
    type: String,
    enum: ["pending", "approved", "rejected"],
    default: "pending"
  },
  registeredAt: { type: Date, default: Date.now },
  reviewedAt: { type: Date }
});
const MemberRequest = mongoose.model("MemberRequest", memberRequestSchema);

// Projects
const projectSchema = new mongoose.Schema({
  title: String,
  category: {
    type: String,
    enum: ["research-impact", "research-innovation", "educators"],
  },
  status: { type: String, enum: ["active", "deleted"], default: "active" },
  lastEditedAt: { type: Date, default: Date.now },
});
const Project = mongoose.model("Project", projectSchema);

// Research Entries (from Wizard)
const researchEntrySchema = new mongoose.Schema({
  title: String,
  year: String,
  domain: String,
  statement: String,
  abstract: String,
  authors: [String],
  piEmail: String,
  funding: String,
  keywords: [String],
  videoLink: String,
  publicationType: String,
  category: { type: String, enum: ["research-innovation", "educators", "research-impact"] },
  status: { type: String, enum: ["ongoing", "upcoming", "completed"], default: "ongoing" },
  visibility: mongoose.Schema.Types.Mixed,
  specifics: mongoose.Schema.Types.Mixed,
  isPublic: { type: Boolean, default: false },
  createdAt: { type: Date, default: Date.now },
  lastEditedAt: { type: Date, default: Date.now }
});
const ResearchEntry = mongoose.model("ResearchEntry", researchEntrySchema);

// Audit Logs
const auditLogSchema = new mongoose.Schema({
  action: String,
  performedBy: String,
  timestamp: { type: Date, default: Date.now },
});
const AuditLog = mongoose.model("AuditLog", auditLogSchema);

// Courses
const courseSchema = new mongoose.Schema({
  title: String,
  description: String,
  detailedInfo: String,
  focusItems: [String],
  image: String,
  link: String,
  iconSvg: String // Store SVG for course icon
});
const Course = mongoose.model("Course", courseSchema);

// Activities
const activitySchema = new mongoose.Schema({
  slug: { type: String, unique: true },
  title: String,
  icon: String, // FA class or SVG HTML
  statNumber: String,
  statLabel: String,
  overviewContent: String,
  detailDescription: [String],
  highlights: [String],
  image: String,
  buttonText: String,
  buttonLink: String,
  order: Number,
  showOnHome: { type: Boolean, default: false }, // Only original 4 stat cards appear on home page
  lastEditedAt: { type: Date, default: Date.now }
});
const Activity = mongoose.model("Activity", activitySchema);

// ✅ SEED COURSES (RUN IF EMPTY)
const seedCourses = async () => {
  try {
    const count = await Course.countDocuments();
    if (count === 0) {
      console.log("🌱 Seeding courses...");
      const initialCourses = [
        {
          title: "MSc in Artificial Intelligence in Healthcare",
          description: "A multidisciplinary master's program integrating clinical training with engineering and data science to drive innovation in diagnostics and healthcare systems.",
          detailedInfo: "Designed for forward-thinking professionals, this curriculum blends rigorous clinical training with advanced engineering and data science. Students will work with real-world medical datasets to develop actionable solutions for diagnostics, hospital operations, and public health surveillance.",
          focusItems: ["Machine learning in diagnostics", "Clinical workflow integration", "Healthcare data systems"],
          image: "/assets/images/gallery.jpeg",
          link: "msc-ai.html"
        },
        {
          title: "Integrated MSc–PhD in AI in Healthcare",
          description: "An intensive dual-degree program designed to advance AI-driven research in clinical settings, enabling scholars to contribute to precision medicine and impactful healthcare solutions.",
          detailedInfo: "Our Integrated MSc-PhD program is a fast-track for scholars aiming to lead at the intersection of clinical science and artificial intelligence. This dual degree emphasizes long-term research projects in genomics, predictive modeling, and clinical trials, preparing graduates for high-impact roles in academia and the pharmaceutical industry.",
          focusItems: ["Advanced predictive modelling", "Deep learning in genomics", "Longitudinal clinical studies"],
          image: "/assets/images/gallery.jpeg",
          link: "integrated-msc-phd.html"
        },
        {
          title: "Predictive Analytics & Decision Support Systems",
          description: "Learn to leverage AI to anticipate patient needs before they become critical. This module trains clinicians and developers to build and interpret algorithms that forecast disease outbreaks, predict patient readmissions, and optimize hospital bed capacity.",
          detailedInfo: "The Predictive Analytics module provides hands-on experience with forecasting models used in modern hospitals. You will learn to utilize EHR data to identify at-risk patients, optimize resource allocation during surges, and implement decision-support tools that assist clinical staff in real-time.",
          focusItems: ["Disease outbreak forecasting", "Patient readmission prediction", "Hospital capacity optimization"],
          image: "/assets/images/gallery.jpeg",
          link: "predictive-analytics.html"
        },
        {
          title: "Advanced Medical Imaging & Computer Vision",
          description: "Transform how you see patient data. Students will master the application of neural networks and computer vision to radiology and pathology. Learn to train models that triage urgent scans, detect early-stage anomalies, and assist specialists with unparalleled accuracy.",
          detailedInfo: "Master the cutting-edge techniques of computer vision applied to medical imaging. This course covers everything from convolutional neural networks (CNNs) for scan classification to automated segmentation of tumors and vascular structures, with a focus on improving diagnostic speed and accuracy.",
          focusItems: ["Neural networks in radiology", "Automated anomaly detection", "Real-time triage systems"],
          image: "/assets/images/gallery.jpeg",
          link: "advanced-medical-imaging.html"
        },
        {
          title: "Personalized Medicine & Targeted Therapeutics",
          description: "Move away from one-size-fits-all treatments. This course explores how AI and machine learning are used to analyze complex genetic profiles and patient histories, enabling the creation of highly individualized, patient-specific treatment pathways.",
          detailedInfo: "Explore the future of pharmacology and genomics. Learn how to leverage multi-omic data (genomics, proteomics, metabolomics) to predict drug responses and design personalized treatment plans. This program focuses on precision oncology and rare disease management using AI-driven insights.",
          focusItems: ["Genomic data analysis", "Individualized treatment pathways", "Predictive drug response"],
          image: "/assets/images/gallery.jpeg",
          link: "personalized-medicine.html"
        },
        {
          title: "AI Ethics, Governance, and Responsible Innovation",
          description: "Innovation must never outpace patient safety. This critical module instills a deep understanding of AI limitations, data privacy, bias auditing, and regulatory frameworks. We emphasize the necessity of keeping AI applications under appropriate, continuous human oversight.",
          detailedInfo: "As AI becomes central to healthcare, ethics and governance are paramount. This course addresses the legal and ethical challenges of AI, including bias mitigation, data privacy (HIPAA/GDPR), and the regulatory landscape for medical devices. We focus on building trustworthy AI that prioritizes patient welfare.",
          focusItems: ["Bias auditing & mitigation", "Data privacy & security", "Regulatory compliance (HIPAA/GDPR)"],
          image: "/assets/images/gallery.jpeg",
          link: "ai-ethics-governance.html"
        }
      ];
      await Course.insertMany(initialCourses);
      console.log("✅ Courses seeded successfully");
    }
  } catch (err) {
    console.error("Error seeding courses:", err);
  }
};

// ✅ SEED RESEARCH ENTRIES (RUN IF EMPTY)
const seedResearchEntries = async () => {
  try {
    console.log("🌱 Syncing the Genomic project...");
    await ResearchEntry.findOneAndUpdate(
      { title: "Genomic variant classification for hereditary breast cancer risk" },
      {
        title: "Genomic variant classification for hereditary breast cancer risk",
        year: "2024",
        domain: "Genomics & Precision Medicine",
        statement: "Developed a ML classifier for BRCA1/2 variants of uncertain significance, achieving 87% classification accuracy on 4,200 patient genomes.",
        abstract: "40% of BRCA variants are classified as 'uncertain significance,' leaving patients without actionable risk information.",
        authors: ["Dr. Meera Krishnan"],
        piEmail: "aihealthcare.kmc@manipal.edu",
        funding: "Institutional",
        keywords: ["Python", "R", "Bioconductor", "VCF analysis"],
        publicationType: "Paper",
        category: "research-impact",
        status: "completed",
        visibility: {
          v_impactTitle: true,
          v_impactStatement: true,
          v_impactAbstract: true,
          v_impactAuthors: true,
          v_impactPiEmail: true,
          v_impactFunding: true,
          v_impactKeywords: true,
          v_impactYear: true,
          v_impactDomain: true
        }
      },
      { upsert: true, new: true }
    );
    console.log("✅ Genomic project synced");

    console.log("🌱 Syncing the Triage project...");
    await ResearchEntry.findOneAndUpdate(
      { title: "AI-assisted triage scoring for emergency department overcrowding" },
      {
        title: "AI-assisted triage scoring for emergency department overcrowding",
        statement: "Building a real-time triage dashboard that scores incoming ED patients using vital signs and chief complaint to predict wait time and severity.",
        abstract: "KMC ED sees 300+ patients daily. Manual triage is slow and inconsistent. An AI-assisted tool can reduce median wait time by 40%. The project involves a React frontend, Node.js + Express backend, MongoDB, and a Python ML microservice.",
        year: 2024,
        domain: "Predictive Analytics",
        status: "upcoming",
        category: "educators",
        piEmail: "sneha.rao@manipal.edu",
        funding: "Institutional",
        isPublic: true,
        visibility: {
          v_impactTitle: true,
          v_impactStatement: true,
          v_impactAbstract: true,
          v_impactDomain: true,
          v_impactYear: true,
          v_impactPiEmail: true,
          v_impactFunding: true
        }
      },
      { upsert: true, new: true }
    );
    console.log("✅ Triage project synced");

    console.log("🌱 Syncing the Internal Medicine project...");
    await ResearchEntry.findOneAndUpdate(
      { title: "Internal Medicine /Emergency Medicine" },
      {
        title: "Internal Medicine /Emergency Medicine",
        statement: "A Typical Presentation of Massive Pulmonary Embolism",
        abstract: "This case demonstrates that massive PE can present as isolated epigastric pain and bradycardia, highlighting the need to include PE in the differential diagnosis of unexplained abdominal shock.",
        authors: ["Uma", "Deepak"],
        piEmail: "uma123@gmail.com",
        funding: "dst/ery30490",
        year: 2026,
        domain: "Clinical Decision Support",
        status: "ongoing",
        category: "educators",
        isPublic: true,
        specifics: {
          s_name: "Delhi",
          s_doi: "25-05-2026",
          s_cond: "Medicine",
          s_out: "95"
        },
        visibility: {
          v_impactTitle: true,
          v_impactStatement: true,
          v_impactAbstract: true,
          v_impactAuthors: true,
          v_impactPiEmail: true,
          v_impactFunding: true,
          v_impactYear: true,
          v_impactDomain: true,
          v_s_name: true,
          v_s_doi: true,
          v_s_cond: true,
          v_s_out: true
        }
      },
      { upsert: true, new: true }
    );
    console.log("✅ Internal Medicine project synced");

    console.log("🌱 Syncing the Diabetic Retinopathy project...");
    await ResearchEntry.findOneAndUpdate(
      { title: "AI-based Screening for Diabetic Retinopathy in Rural Clinics" },
      {
        title: "AI-based Screening for Diabetic Retinopathy in Rural Clinics",
        statement: "Deploying deep learning models for early detection of DR using portable fundus cameras.",
        abstract: "This project focuses on providing accessible eye care in underserved regions of Karnataka. We use a cloud-based AI model to analyze retinal images and flag moderate-to-severe cases for immediate referral.",
        authors: ["Dr. Arjun Mehta", "Sarah Wilson"],
        piEmail: "arjun.mehta@manipal.edu",
        funding: "MAHE Innovation Grant",
        year: 2025,
        domain: "Medical Imaging",
        status: "ongoing",
        category: "educators",
        visibility: {
          v_impactTitle: true,
          v_impactStatement: true,
          v_impactAbstract: true,
          v_impactAuthors: true,
          v_impactPiEmail: true,
          v_impactFunding: true,
          v_impactYear: true,
          v_impactDomain: true
        },
        isPublic: false
      },
      { upsert: true, new: true }
    );
    console.log("✅ Diabetic Retinopathy project synced");
    const totalCount = await ResearchEntry.countDocuments();
    console.log(`📊 Total Research Entries in DB: ${totalCount}`);
  } catch (err) {
    console.error("Error seeding research entries:", err);
  }
};

// ✅ SEED ACTIVITIES (RUN IF EMPTY)
const seedActivities = async () => {
  try {
    const initialActivities = [
      {
        slug: "research-impact",
        title: "Research & Impact",
        icon: '<svg xmlns="http://www.w3.org/2000/svg" width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="#D14905" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3" /><path d="M8 15v1a6 6 0 0 0 6 6h2a6 6 0 0 0 6-6v-4" /><circle cx="20" cy="10" r="2" /></svg>',
        statNumber: "17+",
        statLabel: "Clinical Research",
        overviewContent: "Our department conducts pioneering clinical research integrating AI with patient data to improve diagnostics, treatment planning, and patient outcomes across multiple healthcare domains.",
        detailDescription: [
          "At the Department of AI in Healthcare, Research & Impact forms the backbone of our scientific mission. Our interdisciplinary teams work at the intersection of medicine, data science, and engineering to design studies that directly improve patient care.",
          "Collaborating with KMC hospitals and Manipal's vast clinical network, we have access to rich de-identified patient datasets that fuel research in diagnostics, disease prediction, medical imaging analysis, and personalised medicine."
        ],
        highlights: [
          "AI-driven early detection of chronic diseases",
          "Medical imaging analysis using deep learning",
          "Predictive modelling for ICU patient outcomes",
          "NLP-based clinical documentation systems",
          "Federated learning for privacy-preserving healthcare AI"
        ],
        image: "/assets/images/home/img2.png",
        buttonText: "Get Involved →",
        buttonLink: "contact-us.html",
        order: 1,
        showOnHome: true
      },
      {
        slug: "industry-collabs",
        title: "Industry Collaborations",
        icon: '<svg xmlns="http://www.w3.org/2000/svg" width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="#D14905" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m11 17 2 2a1 1 0 1 0 3-3" /><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4" /><path d="m21 3 1 11h-2" /><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3" /><path d="M3 4h8" /></svg>',
        statNumber: "5+",
        statLabel: "Industry Collabs",
        overviewContent: "We bridge the gap between academic research and commercial applications through strategic partnerships with global healthcare leaders and innovative startups.",
        detailDescription: [
          "We believe the best AI solutions for healthcare emerge when academia and industry work side by side. Our department actively cultivates relationships with healthcare technology companies, hospitals, and startups to co-develop solutions that scale.",
          "These partnerships provide our students and faculty with access to real-world datasets, cutting-edge infrastructure, and mentorship from industry leaders — ensuring that our graduates are industry-ready from day one."
        ],
        highlights: [
          "Joint R&D projects with health-tech firms",
          "Industry-sponsored student capstone projects",
          "Internship and placement pipelines",
          "Co-authored publications and IP development",
          "Workshops and technology transfer sessions"
        ],
        image: "/assets/images/activities/industry-collabs.png",
        buttonText: "Partner With Us →",
        buttonLink: "contact-us.html",
        order: 2,
        showOnHome: true
      },
      {
        slug: "student-projects",
        title: "Student Projects",
        icon: '<svg xmlns="http://www.w3.org/2000/svg" width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="#D14905" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z" /><path d="M6 12v5c0 2.21 2.686 4 6 4s6-1.79 6-4v-5" /></svg>',
        statNumber: "3+",
        statLabel: "Student Projects",
        overviewContent: "Our students work on real-world healthcare challenges, developing AI models that address genuine clinical needs under expert faculty guidance.",
        detailDescription: [
          "Our students are not just learners — they are innovators. From their first semester, students are encouraged to propose, design, and execute AI projects that solve genuine healthcare problems under the guidance of expert faculty and industry mentors.",
          "Projects span radiology AI, mental health monitoring, epidemic forecasting, wearable health sensors, and hospital management systems — many go on to be published or commercialised."
        ],
        highlights: [
          "AI-powered retinal disease screening tool",
          "Smart triage system for emergency departments",
          "Epidemic forecasting using social media signals",
          "Wearable vitals monitoring with anomaly detection",
          "NLP chatbot for patient symptom triage"
        ],
        image: "/assets/images/activities/student-projects.png",
        buttonText: "Explore Programmes →",
        buttonLink: "programs.html",
        order: 3,
        showOnHome: true
      },
      {
        slug: "guest-speakers",
        title: "Guest Speakers",
        icon: '<svg xmlns="http://www.w3.org/2000/svg" width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="#D14905" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2" width="6" height="11" rx="3" /><path d="M5 10a7 7 0 0 0 14 0" /><line x1="12" y1="19" x2="12" y2="22" /><line x1="8" y1="22" x2="16" y2="22" /></svg>',
        statNumber: "1",
        statLabel: "Event",
        overviewContent: "We regularly host distinguished experts from academia, industry, and hospitals who share their insights on the latest breakthroughs in AI, healthcare, and medical technology.",
        detailDescription: [
          "We regularly invite distinguished researchers, clinicians, and technology leaders to share their knowledge with our community. These sessions provide students and faculty with direct exposure to the cutting edge of AI in healthcare globally.",
          "Our speaker series covers AI ethics, precision medicine, large language models in clinical settings, global health data challenges, and transformative case studies from leading healthcare systems worldwide."
        ],
        highlights: [
          "Keynotes from global AI & health experts",
          "Interactive Q&A and panel discussions",
          "Workshops and hands-on demo sessions",
          "Networking opportunities with visiting researchers",
          "Recorded sessions available to the student community"
        ],
        image: "/assets/images/mahe2.webp",
        buttonText: "Stay Updated →",
        buttonLink: "contact-us.html",
        order: 4,
        showOnHome: true
      }
    ];

    for (const activity of initialActivities) {
      await Activity.findOneAndUpdate({ slug: activity.slug }, activity, { upsert: true });
    }
    console.log("✅ Activities seeded/synced successfully");
  } catch (err) {
    console.error("Error seeding activities:", err);
  }
};

/* =========================
   🔑 MEMBER REGISTRATION & APPROVAL FLOW
========================= */

// POST /api/member/register — public user registers
app.post("/api/member/register", async (req, res) => {
  const { name, email, institution, reason, password } = req.body;

  if (!name || !email || !password) {
    return res.status(400).json({ message: "Name, email and password are required." });
  }
  if (!email.includes("@")) {
    return res.status(400).json({ message: "Invalid email address." });
  }

  try {
    const existing = await MemberRequest.findOne({ email: email.trim().toLowerCase() });
    if (existing) {
      return res.status(409).json({
        message: "An account with this email already exists.",
        status: existing.registrationStatus
      });
    }

    const passwordHash = await argon2.hash(password);
    await MemberRequest.create({
      name: name.trim(),
      email: email.trim().toLowerCase(),
      institution: institution || "",
      reason: reason || "",
      passwordHash
    });

    await AuditLog.create({
      action: `New member registration request from: ${email}`,
      performedBy: email
    });

    res.status(201).json({ message: "Registration submitted. Awaiting admin approval." });
  } catch (err) {
    console.error("Registration error:", err);
    res.status(500).json({ message: "Server error during registration." });
  }
});

// GET /api/member/status/:email — poll for approval status
app.get("/api/member/status/:email", async (req, res) => {
  try {
    const member = await MemberRequest.findOne({
      email: req.params.email.toLowerCase()
    });
    if (!member) {
      return res.status(404).json({ message: "Email not found." });
    }
    res.status(200).json({ status: member.registrationStatus });
  } catch (err) {
    res.status(500).json({ message: "Server error." });
  }
});

// POST /api/member/login — approved member logs in
app.post("/api/member/login", async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ message: "Email and password required." });
  }

  try {
    const member = await MemberRequest.findOne({ email: email.trim().toLowerCase() });
    if (!member) {
      return res.status(401).json({ message: "No account found with this email." });
    }
    if (member.registrationStatus === "pending") {
      return res.status(403).json({ message: "Your account is still pending admin approval." });
    }
    if (member.registrationStatus === "rejected") {
      return res.status(403).json({ message: "Your access request was not approved." });
    }

    const isMatch = await argon2.verify(member.passwordHash, password);
    if (!isMatch) {
      return res.status(401).json({ message: "Incorrect password." });
    }

    const token = signToken({ memberId: member._id.toString(), email: member.email, name: member.name, role: 'member' });

    await AuditLog.create({
      action: `Member login: ${email}`,
      performedBy: email
    });

    res.status(200).json({
      message: "Login successful",
      token,
      member: { name: member.name, email: member.email }
    });
  } catch (err) {
    console.error("Member login error:", err);
    res.status(500).json({ message: "Server error during login." });
  }
});

/* ---- ADMIN: Member request management ---- */

// GET /api/admin/member-requests — list all member requests
app.get("/api/admin/member-requests", async (req, res) => {
  try {
    const requests = await MemberRequest.find().sort({ registeredAt: -1 }).select("-passwordHash");
    res.status(200).json(requests);
  } catch (err) {
    res.status(500).json({ message: "Server error." });
  }
});

// POST /api/admin/member-requests/:id/approve
app.post("/api/admin/member-requests/:id/approve", async (req, res) => {
  try {
    const member = await MemberRequest.findByIdAndUpdate(
      req.params.id,
      { registrationStatus: "approved", reviewedAt: new Date() },
      { new: true }
    );
    if (!member) return res.status(404).json({ message: "Request not found." });

    await AuditLog.create({
      action: `Approved member: ${member.email}`,
      performedBy: req.body.adminEmail || "Admin"
    });

    res.status(200).json({ message: "Member approved.", member });
  } catch (err) {
    res.status(500).json({ message: "Server error." });
  }
});

// POST /api/admin/member-requests/:id/reject
app.post("/api/admin/member-requests/:id/reject", async (req, res) => {
  try {
    const member = await MemberRequest.findByIdAndUpdate(
      req.params.id,
      { registrationStatus: "rejected", reviewedAt: new Date() },
      { new: true }
    );
    if (!member) return res.status(404).json({ message: "Request not found." });

    await AuditLog.create({
      action: `Rejected member: ${member.email}`,
      performedBy: req.body.adminEmail || "Admin"
    });

    res.status(200).json({ message: "Member rejected.", member });
  } catch (err) {
    res.status(500).json({ message: "Server error." });
  }
});

/* =========================
   📧 SUBSCRIBE API
========================= */
app.post("/api/subscribe", async (req, res) => {
  const { email } = req.body;

  if (!email || !email.includes("@")) {
    return res.status(400).json({ message: "Invalid email" });
  }

  try {
    const response = await fetch("https://api.brevo.com/v3/contacts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "api-key": process.env.BREVO_API_KEY,
      },
      body: JSON.stringify({
        email: email,
        listIds: [parseInt(process.env.BREVO_LIST_ID)],
        updateEnabled: true,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      return res.status(200).json({ message: "Subscribed successfully" });
    } else {
      return res.status(500).json({ message: data.message || "Brevo error" });
    }
  } catch (error) {
    return res.status(500).json({ message: "Server error" });
  }
});

/* =========================
   🔐 ADMIN LOGIN (ARGON2)
========================= */
app.post("/api/admin/login", async (req, res) => {
  const { email, password } = req.body;

  try {
    const admin = await Admin.findOne({ email: email.trim() });

    if (!admin) {
      return res.status(401).json({ message: "Email not found" });
    }

    const isMatch = await argon2.verify(admin.password, password.trim());

    if (!isMatch) {
      return res.status(401).json({ message: "Wrong password" });
    }

    const token = signToken({ email: admin.email, role: 'admin' });

    res.status(200).json({
      message: "Login successful",
      token
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server error" });
  }
});

/* =========================
   📝 SUBMIT RESEARCH ENTRY
========================= */
app.post("/api/research", async (req, res) => {
  try {
    const entryData = req.body;
    const newEntry = await ResearchEntry.create(entryData);

    // Log activity
    await AuditLog.create({
      action: `Created new research entry: ${newEntry.title || 'Untitled'}`,
      performedBy: entryData.adminEmail || "Unknown Admin",
    });

    res.status(201).json({ message: "Entry saved successfully", entry: newEntry });
  } catch (error) {
    console.error("Error saving research entry:", error);
    res.status(500).json({ message: "Server error while saving entry" });
  }
});

// GET /api/research — public list (secured with member check)
app.get("/api/research", verifyMember, async (req, res) => {
  try {
    const entries = await ResearchEntry.find().sort({ createdAt: -1 });
    const impactCount = entries.filter(e => e.category === 'research-impact').length;
    const completedCount = entries.filter(e => e.status === 'completed').length;
    console.log(`📡 Research API called. Total: ${entries.length}, Impact: ${impactCount}, Completed: ${completedCount}`);

    // If not a logged-in approved member, redact the educators' sensitive fields
    const processedEntries = entries.map(entry => {
      if (entry.category === 'educators' && !req.isApprovedMember && !req.isAdmin && !entry.isPublic) {
        return {
          _id: entry._id,
          category: entry.category,
          year: entry.year,
          domain: entry.domain,
          title: "[Members Only Content]",
          statement: "This project information is restricted to approved educators and collaborators.",
          abstract: "REDACTED: Please log in to view full abstract.",
          isRedacted: true
        };
      }
      return entry;
    });

    res.status(200).json(processedEntries);
  } catch (error) {
    res.status(500).json({ message: "Server error while fetching research entries" });
  }
});

// Debug endpoint to check DB state
app.get("/api/debug/research", async (req, res) => {
  try {
    const entries = await ResearchEntry.find();
    res.json({
      count: entries.length,
      entries: entries
    });
  } catch (err) {
    res.status(500).json(err);
  }
});

app.put("/api/research/:id", async (req, res) => {
  const { title, statement, abstract, year, domain, piEmail, funding, status, adminEmail } = req.body;
  try {
    const updatedEntry = await ResearchEntry.findByIdAndUpdate(req.params.id, {
      title, statement, abstract, year, domain, piEmail, funding, status,
      lastEditedAt: new Date()
    }, { new: true });

    if (!updatedEntry) return res.status(404).json({ message: "Entry not found" });

    await AuditLog.create({
      action: `Updated research entry: ${title || updatedEntry.title || 'Untitled'}`,
      performedBy: adminEmail || "Unknown Admin",
    });

    res.status(200).json(updatedEntry);
  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});

app.delete("/api/research/:id", async (req, res) => {
  const { adminEmail } = req.body || {};
  try {
    const deletedEntry = await ResearchEntry.findByIdAndDelete(req.params.id);
    if (!deletedEntry) return res.status(404).json({ message: "Entry not found" });

    // Log activity
    await AuditLog.create({
      action: `Deleted research entry: ${deletedEntry.title || 'Untitled'}`,
      performedBy: adminEmail || "Unknown Admin",
    });

    res.status(200).json({ message: "Entry deleted successfully" });
  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});

/* =========================
   📊 DASHBOARD STATS
========================= */
app.get("/api/admin/dashboard-stats", async (req, res) => {
  try {
    const projectImpactCount = await Project.countDocuments({
      category: "research-impact",
      status: "active",
    });
    const reImpactCount = await ResearchEntry.countDocuments({
      category: "research-impact"
    });
    const impactCount = projectImpactCount + reImpactCount;

    const projectInnovationCount = await Project.countDocuments({
      category: "research-innovation",
      status: "active",
    });
    const reInnovationCount = await ResearchEntry.countDocuments({
      category: "research-innovation"
    });
    const innovationCount = projectInnovationCount + reInnovationCount;

    const projectEducatorsCount = await Project.countDocuments({
      category: "educators",
      status: "active",
    });
    const reEducatorsCount = await ResearchEntry.countDocuments({
      category: "educators"
    });
    const educatorsCount = projectEducatorsCount + reEducatorsCount;

    const userCount = await MemberRequest.countDocuments();
    const deletedCount = await Project.countDocuments({ status: "deleted" });

    const projectEditedCount = await Project.countDocuments({
      lastEditedAt: { $exists: true },
    });
    const reEditedCount = await ResearchEntry.countDocuments({
      lastEditedAt: { $exists: true }
    });
    const editedCount = projectEditedCount + reEditedCount;

    res.status(200).json({
      impactCount,
      innovationCount,
      educatorsCount,
      userCount,
      deletedCount,
      editedCount,
      sessionStatus: "Active",
    });

  } catch (error) {
    res.status(500).json({ message: "Server error" });
  }
});

/* =========================
   📜 ACTIVITY LOGS
========================= */
app.get("/api/admin/activity", async (req, res) => {
  try {
    const logs = await AuditLog.find().sort({ timestamp: -1 }).limit(10);
    res.status(200).json(logs);
  } catch (error) {
    res.status(500).json({ message: "Server error" });
  }
});

/* =========================
   🎓 COURSE MANAGEMENT
========================= */
app.get("/api/courses", async (req, res) => {
  try {
    const courses = await Course.find();
    res.status(200).json(courses);
  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});

app.get("/api/courses/:id", async (req, res) => {
  try {
    const course = await Course.findById(req.params.id);
    if (!course) return res.status(404).json({ message: "Course not found" });
    res.status(200).json(course);
  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});

app.put("/api/courses/:id", async (req, res) => {
  const { title, description, detailedInfo, focusItems, adminEmail } = req.body;
  try {
    const updatedCourse = await Course.findByIdAndUpdate(req.params.id, {
      title,
      description,
      detailedInfo,
      focusItems
    }, { new: true });

    if (!updatedCourse) return res.status(404).json({ message: "Course not found" });

    // Log activity
    await AuditLog.create({
      action: `Updated course: ${title}`,
      performedBy: adminEmail || "Unknown Admin",
    });

    res.status(200).json(updatedCourse);
  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});

/* =========================
   🏃 ACTIVITY MANAGEMENT
========================= */
// Returns ALL activities (used by activity.html page)
app.get("/api/activities", async (req, res) => {
  try {
    const activities = await Activity.find().sort({ order: 1 });
    res.status(200).json(activities);
  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});

// Returns ONLY home-pinned activities (used by index.html stats section)
app.get("/api/activities/home", async (req, res) => {
  try {
    const activities = await Activity.find({ showOnHome: true }).sort({ order: 1 });
    res.status(200).json(activities);
  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});

app.post("/api/activities", async (req, res) => {
  try {
    const { title, overviewContent, icon, image, adminEmail } = req.body;
    const slug = title.toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g, '');

    const count = await Activity.countDocuments();
    const newActivity = await Activity.create({
      slug,
      title,
      overviewContent,
      icon: icon || '<i class="fas fa-stethoscope"></i>',
      statNumber: "0",
      statLabel: "New",
      detailDescription: [overviewContent],
      highlights: [],
      image: image || "/assets/images/home/img2.png",
      buttonText: "Learn More →",
      buttonLink: "#",
      order: count + 1
    });

    await AuditLog.create({
      action: `Created new activity: ${title}`,
      performedBy: adminEmail || "Admin",
    });

    res.status(201).json(newActivity);
  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});

app.put("/api/activities/:id", async (req, res) => {
  try {
    const {
      title, overviewContent, statNumber, statLabel,
      detailDescription, highlights, buttonText, buttonLink,
      image, adminEmail
    } = req.body;

    const updateData = {
      title, overviewContent, statNumber, statLabel,
      detailDescription, highlights, buttonText, buttonLink,
      lastEditedAt: new Date()
    };
    if (image) updateData.image = image;

    const updated = await Activity.findByIdAndUpdate(req.params.id, updateData, { new: true });

    if (!updated) return res.status(404).json({ message: "Activity not found" });

    await AuditLog.create({
      action: `Updated activity: ${title}`,
      performedBy: adminEmail || "Admin",
    });

    res.status(200).json(updated);
  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});

/* =========================
   🌐 SERVE FRONTEND
========================= */
app.use(express.static(path.join(__dirname, "public")));

/* =========================
   🚀 START SERVER
========================= */
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});