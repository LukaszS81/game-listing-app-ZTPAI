/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      // proxy any /games/* client request to Django
      {
        source: '/games/:path*',
        destination: 'http://localhost:8000/api/games/:path*',
      },
    ];
  },
}

module.exports = nextConfig
