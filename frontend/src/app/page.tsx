import Image from "next/image";

export default function Home() {
  return (
    <main className="max-w-xs px-6 h-screen w-screen mx-auto flex flex-col items-center justify-center">
        <Image src="/logo.png" alt="Logo" width={100} height={100} />
        <h1 className="text-4xl mt-2 font-bold bg-gradient-to-r from-neutral-500 to-neutral-900 bg-clip-text text-transparent">Croissant AI</h1>
        <p className="text-neutral-800 text-xl mx-auto text-center leading-6 mt-2">Genera un Podcast a partir de un tema.</p>
        <Image className="w-full rounded-2xl mt-8" src="/qr.png" alt="QR Code" layout="responsive" width={100} height={100} />
        <a href="https://t.me/CroissantAI_bot" target="_blank" rel="noopener noreferrer" className="mx-auto text-center bg-gradient-to-r from-[#28A7E8] to-[#24A2DF] text-white px-4 py-1 rounded-full mt-6 text-lg">t.me/CroissantAI_bot</a>
    </main>
  );
}
