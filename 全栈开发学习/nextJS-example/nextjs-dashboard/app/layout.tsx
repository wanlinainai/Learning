import '@/app/ui/global.css';
import {inter} from '@/app/ui/fonts'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      {/* 将Inter添加到body中，该字体会应用于整个应用程序 */}
      <body className={`${inter.className} antialliased`}>{children}</body>
    </html>
  );
}
