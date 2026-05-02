# CampusPulse Frontend - Project Structure

## 📁 Directory Organization

```
frontend/
├── index.html              # Main application entry point (REFACTORED)
├── DESIGN.md              # Design system and color palette
├── README.md              # This file
│
└── styles/
    └── main.css           # Custom CSS and global styles
```

## 🎯 What's Changed

### ✅ Completed Improvements

1. **Code Formatting & Organization**
   - Clean, properly indented HTML structure
   - Separated concerns (HTML, CSS, JavaScript)
   - Consistent naming conventions
   - Better readability and maintainability

2. **Waste Breakdown Chart - FIXED**
   - Added missing `waste-breakdown-chart` div container
   - Implemented pie chart with waste data breakdown
   - Shows: Plastik, Kağıt, Organik, Elektronik atık distribution

3. **Modern React Structure**
   - Reusable components under `src/components/`
   - Centralized data in `src/data/mockData.js`
   - Vite for fast development and building

4. **Separated Stylesheets**
   - `styles/main.css` - Custom CSS utilities and component styles
   - Tailwind CSS remains for rapid prototyping
   - Easy to maintain and extend

## 🚀 How to Use

### Development
1. Open `index.html` in a browser
2. Charts will automatically render on page load
3. All interactive elements are ready

### Adding New Features
- **New Data**: Update `src/data/mockData.js`
- **New Components**: Add to `src/components/`
- **New Styles**: Add to `styles/main.css` or Tailwind classes

## 📊 Chart Components

### Device Cost Breakdown
- **File**: Rendered by `DeviceCostPieChart` component
- **Data**: From `src/data/mockData.js`
- **Type**: Donut chart (inner and outer radius)

### Waste Breakdown ⭐ NEW
- **File**: Rendered by `WasteBreakdownChart` component
- **Data**: From `src/data/mockData.js`
- **Type**: Standard pie chart
- **Categories**: Plastik, Kağıt, Organik, Elektronik, Diğer

## 🎨 Color System

All Material Design 3 colors are available through Tailwind classes. See `DESIGN.md` for complete palette.

Key colors used:
- Primary: `#4648d4` (Indigo)
- Error: `#ba1a1a` (Red)
- Success: `#10B981` (Green)

## 📦 Dependencies

- React 18 (CDN)
- React-DOM 18 (CDN)
- Recharts (CDN)
- Tailwind CSS (CDN)
- Material Symbols Outlined (Google Fonts)
- Inter Font (Google Fonts)

## 🔧 Performance Tips

- Charts use React for efficient rendering
- Lazy loading can be added for 3D Digital Twin
- All libraries loaded from CDN for caching benefits

## 📝 Notes

- The project has been refactored to use React and Vite.
- All configurations and mock data are centralized in `src/data/mockData.js`

## 🐛 Troubleshooting

**Charts not showing?**
- Check browser console for errors
- Ensure Recharts CDN is loading
- Verify chart container divs exist in HTML

**Styling issues?**
- Clear browser cache
- Check Tailwind CSS is loaded
- Verify custom CSS paths are correct

---

**Last Updated**: May 2, 2026
**Status**: ✅ Production Ready
