//Vite의 모든 설정을 담는 중앙 컨트롤 파일이야.
//여기에 내 리액트 앱이 어떻게 동작하고 어떤 플러그인을 쓰는지에 대한 설정이 담겨 있음.  


import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
// import { VitePWA } from 'vite-plugin-pwa'

// // https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server:{
    host:true
  }
})

// PWA 플러그인은 빌드 이슈로 인해 일시적으로 비활성화
// export default defineConfig({
//   plugins: [
//     react(),
//     VitePWA({
//       registerType: 'autoUpdate',
//       manifest: {
//         name: '나의 멋진 앱',
//         short_name: '앱이름',
//         start_url: '/',
//         display: 'standalone',
//         background_color: '#ffffff',
//         theme_color: '#000000',
//         icons: [
//           {
//             src: '/icon-192x192.png',
//             sizes: '192x192',
//             type: 'image/png'
//           },
//           {
//             src: '/icon-512x512.png',
//             sizes: '512x512',
//             type: 'image/png'
//           }
//           
//         ]
//       }
//     })
//   ],
//   server:{
//     host:true
//   }
// })

//npm run build 이게 프로젝트를 빌드(정적 파일)로 변환하기.
//->이게 dist 폴더 안에 생긴다