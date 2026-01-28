# 🚀 AI Tool Discovery Platform

> **Automated SaaS platform that discovers, analyzes, and tracks trending AI tools daily**

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_Site-blue?style=for-the-badge)](https://yovaan-ai-tools.netlify.app/)

---

## 📸 Screenshots

![Dashboard](<img width="1837" height="982" alt="image" src="https://github.com/user-attachments/assets/8d390d6d-ab74-4a69-a3c8-b03063d9f7da" />)
*Dashboard showing trending AI tools with real-time statistics*


---

## ✨ Features

🔍 **Automated Discovery**
- Scrapes 50+ AI tools daily from GitHub Trending, Product Hunt, and Hugging Face
- Completely autonomous - runs daily at 12:00 PM UTC via GitHub Actions
- Intelligent filtering to identify AI/ML-specific projects

🤖 **AI-Powered Analysis**
- Automatic summarization using Hugging Face Transformers
- Smart categorization (NLP, Computer Vision, Audio, etc.)
- Hype score algorithm based on stars, likes, and engagement
- Pricing detection (Free, Freemium, Paid)

📊 **Beautiful Dashboard**
- Real-time statistics and trending tools
- Advanced filtering by category and pricing
- Responsive design (mobile, tablet, desktop)
- Fast, optimized performance with Next.js

⚡ **Production-Ready**
- 99%+ uptime with cloud hosting
- Automated CI/CD pipeline
- Secure API key management
- Error handling and logging
- RESTful API with auto-generated documentation

---

## 🛠️ Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue?logo=postgresql)

- **FastAPI** - Modern, high-performance web framework
- **BeautifulSoup4** - HTML parsing and web scraping
- **Hugging Face Transformers** - AI-powered text analysis
- **Supabase** - PostgreSQL database with real-time capabilities
- **APScheduler** - Task scheduling and automation

### Frontend
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![React](https://img.shields.io/badge/React-18-blue?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![Tailwind](https://img.shields.io/badge/Tailwind-3-cyan?logo=tailwindcss)

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Beautiful icon library

### DevOps & Infrastructure
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-black?logo=github)
![netlify](https://img.shields.io/badge/Vercel-Hosting-black?logo=vercel)
![Render](https://img.shields.io/badge/Render-API_Hosting-purple?logo=render)

- **GitHub Actions** - Automated daily scraping
- **netlify** - Frontend hosting with edge network
- **Render** - Backend API hosting with auto-scaling
- **Git** - Version control

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY AUTOMATION                          │
│  (Runs automatically every 24 hours via GitHub Actions)      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   WEB SCRAPER          │
        │ • GitHub Trending      │
        │ • Product Hunt         │
        │ • Hugging Face         │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │   AI ANALYZER          │
        │ • Summarization        │
        │ • Categorization       │
        │ • Hype Score Calc      │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │   DATABASE             │
        │ PostgreSQL (Supabase)  │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │   FASTAPI BACKEND      │
        │ RESTful API            │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │   NEXT.JS FRONTEND     │
        │ Interactive Dashboard  │
        └────────────────────────┘
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tools` | GET | Get all tools (with filters) |
| `/api/tools/trending` | GET | Get today's trending tools |
| `/api/tools/{id}` | GET | Get specific tool details |
| `/api/stats` | GET | Dashboard statistics |
| `/api/categories` | GET | List all categories |
| `/api/scan/manual` | POST | Trigger manual scan |



---

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- Supabase account (free)

### Backend Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ai-tool-tracker.git
cd ai-tool-tracker/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials

# Run server
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend Setup
```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Setup environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev
```

Frontend runs on `http://localhost:3000`

---

## 🗄️ Database Schema
```sql
CREATE TABLE ai_tools (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    url TEXT NOT NULL,
    source TEXT NOT NULL,
    category TEXT,
    hype_score INTEGER,
    github_stars INTEGER,
    pricing TEXT,
    use_cases TEXT[],
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_hype_score ON ai_tools(hype_score DESC);
CREATE INDEX idx_category ON ai_tools(category);
CREATE INDEX idx_discovered_date ON ai_tools(discovered_date DESC);
```

---

## 🔒 Environment Variables

### Backend (.env)
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
HUGGINGFACE_API_KEY=your_hf_token  # Optional but recommended
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=your_backend_url
```

---

## 📈 Key Learnings & Achievements

### Backend Development
✅ Built production-ready RESTful APIs with FastAPI  
✅ Implemented ethical web scraping with rate limiting  
✅ Integrated third-party APIs (Hugging Face)  
✅ Designed normalized database schemas  
✅ Mastered async/await patterns in Python  

### Frontend Development
✅ Built responsive UIs with React & Next.js 14  
✅ Implemented TypeScript for type safety  
✅ Created reusable component architecture  
✅ Optimized performance with client/server components  

### AI/ML Integration
✅ Used Hugging Face Transformers for NLP tasks  
✅ Implemented custom hype score algorithm  
✅ Automated content categorization  

### DevOps & Deployment
✅ Set up CI/CD with GitHub Actions  
✅ Deployed to production on Vercel + Render  
✅ Configured automated daily jobs  
✅ Managed secrets and environment variables securely  

---

## 🎯 Future Enhancements

- [ ] User authentication and favorites
- [ ] Email notifications for new trending tools
- [ ] Advanced search with Elasticsearch
- [ ] Chrome extension for quick access
- [ ] Community ratings and reviews
- [ ] AI-powered recommendations
- [ ] Export tools as CSV/JSON
- [ ] Integration with more sources (Twitter, Reddit)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


---

## 👨‍💻 Author

**Ravant Vignesh**

- LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/s-ravant-vignesh-384b01373/)


---

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co) for free AI models
- [Supabase](https://supabase.com) for free PostgreSQL database
- [Vercel](https://vercel.com) & [Render](https://render.com) for free hosting
- The amazing open-source community

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you learn something new!

---

<div align="center">

**Built with ❤️ and lots of coffee ☕**

[Live Demo](https://yovaan-ai-tools.netlify.app/)

</div>
```


