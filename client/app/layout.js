import "./globals.css";
import { Toaster } from "sonner";
import Providers from "./libs/providers";

export const metadata = {
  title: "FastAPI Tutorial",
  description: "To learn python fastApi and nextjs",
};



export default function RootLayout({ children }) {
  return (
    <html
      lang="en">
      <body className="min-h-full flex flex-col">
        <Providers>{children}</Providers>
        <Toaster position="bottom-right"  closeButton duration={3000} style={{fontSize: "14px", background:"#0000"}}/>
      </body>
    </html>
  );
}
