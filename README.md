# 🚀 Travel Light - AI-Powered Trip Planning

A modern, intelligent travel planning application that creates personalized itineraries using AI and provides a beautiful, interactive user experience.

## ✨ Features

- **🤖 AI-Powered Planning** - Intelligent trip suggestions and optimization
- **🗺️ Interactive Itinerary Builder** - Drag-and-drop trip planning
- **💾 Database System** - Full CRUD operations with browser storage
- **🎨 Modern UI/UX** - Beautiful, responsive design with shadcn/ui
- **📱 Mobile-First** - Optimized for all devices
- **🔒 Form Validation** - Client-side validation with Zod schemas
- **💾 Auto-Save** - Automatic draft saving and restoration
- **🚀 Performance Optimized** - Caching, deduplication, and lazy loading

## 🏗️ Architecture

```
travel_light_cursor/
├── plan-lighter-ui/          # React frontend application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Application pages
│   │   ├── lib/             # Utilities and services
│   │   │   └── database/    # Database system
│   │   ├── hooks/           # Custom React hooks
│   │   └── store/           # State management
│   └── package.json
├── api_server.py             # FastAPI backend server
├── travel_light.py           # Core AI logic
└── requirements.txt          # Python dependencies
```

## 🛠️ Tech Stack

### **Frontend**
- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Beautiful, accessible components
- **Framer Motion** - Smooth animations
- **React Hook Form** - Form state management
- **Zod** - Schema validation

### **Backend**
- **FastAPI** - Modern Python web framework
- **SQLite/PostgreSQL** - Database support
- **LangGraph** - AI conversation management
- **Uvicorn** - ASGI server

### **Database**
- **Browser Storage** - localStorage for development
- **SQLite** - File-based database
- **PostgreSQL** - Production database (ready)
- **Full CRUD Operations** - Complete data management

## 🚀 Quick Start

### **Prerequisites**
- Node.js 18+ and npm
- Python 3.8+
- Git

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/travel-light.git
cd travel-light
```

### **2. Frontend Setup**
```bash
cd plan-lighter-ui
npm install
npm run dev
```

### **3. Backend Setup**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the API server
python api_server.py
```

### **4. Open Your Browser**
- Frontend: http://localhost:8080
- Backend API: http://localhost:8787
- API Docs: http://localhost:8787/docs

## 📱 Available Pages

- **🏠 Landing** - Welcome and introduction
- **📋 Plan** - Interactive trip planning form
- **🔍 Explore** - Browse activities and destinations
- **🗓️ Itinerary** - View and manage your trip
- **⚙️ Settings** - Application configuration

## 🗄️ Database System

The application includes a comprehensive database system:

- **Browser Storage** - localStorage-based for development
- **SQLite Support** - File-based database
- **PostgreSQL Ready** - Production database configuration
- **Full CRUD Operations** - Create, read, update, delete
- **Search & Filtering** - Advanced query capabilities
- **Statistics & Analytics** - Trip insights and metrics

### **Database Features**
- User management and authentication
- Trip planning and itineraries
- Activity management and scheduling
- Trip sharing and collaboration
- Reviews and ratings system
- Performance monitoring and caching

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file in the project root:

```env
# Development
NODE_ENV=development
DB_TYPE=sqlite

# Production
NODE_ENV=production
DB_TYPE=postgresql
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=travel_light
DB_USER=your_username
DB_PASSWORD=your_password
DB_SSL=true
```

### **API Configuration**
The backend server can be configured via environment variables or command line arguments.

## 🧪 Testing

### **Frontend Testing**
```bash
cd plan-lighter-ui
npm run test
```

### **Database Testing**
Use the built-in database test interface on the Plan page to verify functionality.

## 📦 Building for Production

### **Frontend Build**
```bash
cd plan-lighter-ui
npm run build
```

### **Backend Deployment**
The FastAPI server is production-ready and can be deployed using:
- Docker
- Heroku
- AWS/GCP/Azure
- Traditional VPS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **shadcn/ui** - Beautiful component library
- **Tailwind CSS** - Utility-first CSS framework
- **FastAPI** - Modern Python web framework
- **React Team** - Amazing frontend framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/travel-light/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/travel-light/discussions)
- **Email**: your-email@example.com

## 🚀 Roadmap

- [ ] **User Authentication** - Secure login system
- [ ] **Real-time Collaboration** - Multi-user trip planning
- [ ] **Mobile App** - React Native application
- [ ] **AI Chatbot** - Interactive trip planning assistant
- [ ] **Social Features** - Share and discover trips
- [ ] **Advanced Analytics** - Trip insights and recommendations

---

**Happy Travel Planning! ✈️🗺️**

Made with ❤️ by the Travel Light Team
