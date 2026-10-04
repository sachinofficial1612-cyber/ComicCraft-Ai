/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0284c7',
          600: '#0284c7',
          700: '#0369a1',
          900: '#0c4a6e',
        },
        comic: {
          yellow: '#fde047',
          red: '#ef4444',
          blue: '#3b82f6',
          dark: '#0f172a',
          card: '#1e293b'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        comic: ['Bangers', 'Impact', 'Comic Sans MS', 'sans-serif']
      }
    },
  },
  plugins: [],
}
