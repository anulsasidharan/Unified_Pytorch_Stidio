/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    optimizePackageImports: ["recharts", "mermaid", "react-markdown"],
  },
};

export default nextConfig;
