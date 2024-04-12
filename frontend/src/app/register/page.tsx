"use client";

import { ExternalLink, LoaderIcon } from "lucide-react";
import Image from "next/image";
import { useState } from "react";

export default function Register() {
    const [loading, setLoading] = useState(false);
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setLoading(true);
        // GET parameter telegram_id
        const urlParams = new URLSearchParams(window.location.search);
        const telegram_id = urlParams.get("telegram_id");
        const chat_id = urlParams.get("chat_id");

        const form = event.currentTarget;
        const formData = new FormData(form);
        // POST request to API
        fetch("/api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: formData.get("name"),
                telegram_id: telegram_id,
                chat_id: chat_id,
            }),
        })
            .then((response) => {
                if (response.ok) {
                    window.location.href = "https://t.me/CroissantAI_bot";
                } else {
                    alert("Error al registrar el usuario.");
                    setLoading(false);
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error al registrar el usuario.");
                setLoading(false);
            });
    };
    return (
        <main className="max-w-xs px-6 h-screen w-screen mx-auto flex flex-col items-center justify-center">
            <Image src="/logo.png" alt="Logo" width={100} height={100} />
            <h1 className="text-4xl mt-2 font-bold bg-gradient-to-r from-neutral-500 to-neutral-900 bg-clip-text text-transparent">
                Croissant AI
            </h1>
            <p className="text-neutral-800 text-xl mx-auto text-center leading-6 mt-2">
                Genera un Podcast a partir de un tema.
            </p>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Nombre"
                    name="name"
                    className="w-full mt-4 px-4 py-2 border border-neutral-300 rounded-lg focus:outline-none focus:border-neutral-500"
                    required
                />
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full mt-4 bg-gradient-to-r flex items-center gap-2 justify-center from-[#28A7E8] to-[#24A2DF] text-white px-4 py-2 rounded-lg text-lg"
                >
                    {loading ? (
                        <>
                            Cargando...{" "}
                            <LoaderIcon className="w-5 h-auto animate-spin" />
                        </>
                    ) : (
                        <>
                            Abrir Telegram{" "}
                            <ExternalLink className="w-5 -mt-0.5 h-auto" />
                        </>
                    )}
                </button>
            </form>
        </main>
    );
}
