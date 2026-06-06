/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "standalone",
  experimental: {
    optimizePackageImports: ["recharts", "mermaid", "react-markdown"],
  },
};

export default nextConfig;
