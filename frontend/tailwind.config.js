/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          deep: '#0b3d2e',
          mint: '#0ea371',
          sand: '#f6f4ee',
          ink: '#13221d'
        }
      },
      boxShadow: {
        soft: '0 10px 30px rgba(14, 163, 113, 0.12)'
      }
    },
  },
  plugins: [],
};