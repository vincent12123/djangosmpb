<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a Django project for SMP Negeri 2 student admission (PPDB) with SEO landing page, registration, login, and student dashboard. Registration form must match Dapodik SMP Indonesia requirements.

# Gemini ai

| Language | Library lama         | Library baru (Direkomendasikan) |
|----------|----------------------|---------------------------------|
| Python   | google-generativeai   | google-genai                    |


# Style Guidelines
- Always use Tailwind CSS for all styling - no custom CSS files
- Use utility-first approach with Tailwind classes
- Follow Indonesian government web design standards for educational institutions
- Use responsive design patterns (mobile-first approach)
- Implement dark mode support using Tailwind's dark: prefix

# Django Specific Instructions
- Use Django's template inheritance system
- Follow Django best practices for static file handling
- Use Django forms for all user input validation
- Implement proper CSRF protection
- Use Django's built-in authentication system

# Tailwind CSS Conventions
- Use semantic color classes (bg-blue-500, text-gray-700)
- Implement consistent spacing using Tailwind's spacing scale (p-4, m-2, etc.)
- Use Tailwind's grid system for layouts
- Apply hover and focus states for interactive elements
- Use Tailwind's typography plugin for content areas

# Component Structure
- Create reusable Django template components
- Use Tailwind's component classes (@apply directive when needed)
- Implement consistent button styles across the application
- Use Tailwind's form styling for all input elements

# PPDB Specific Requirements
- Registration forms must include all Dapodik required fields
- Implement proper validation for Indonesian student data (NISN, NIK)
- Use Indonesian language for all user-facing text
- Follow accessibility standards for government websites
- Implement proper error handling and user feedback

# Code Organization
- Keep templates organized in app-specific folders
- Use Django's static files system for Tailwind CSS
- Implement proper URL namespacing
- Use Django's translation system for multi-language support

# Performance
- Optimize Tailwind CSS build for production
- Use Django's caching framework
- Implement lazy loading for images
- Minimize database queries using Django ORM best practices
