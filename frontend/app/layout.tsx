import type { Metadata } from "next";
import { Geist, Geist_Mono, Cinzel_Decorative } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const cinzel = Cinzel_Decorative({
  weight: ["700"],
  variable: "--font-cinzel",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Saga",
  description: "A dynamic and interactive story game.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.className} ${geistMono.className} antialiased`}
      >
        <header className="my-4 flex items-center justify-center text-4xl font-bold tracking-wider">
          <Link
            href="/"
            className={` ${cinzel.className} block text-2xl tracking-widest uppercase antialiased drop-shadow-lg drop-shadow-neutral-500 hover:text-neutral-300 sm:text-3xl md:text-4xl`}
          >
            Saga
          </Link>
        </header>
        {children}
      </body>
    </html>
  );
}
