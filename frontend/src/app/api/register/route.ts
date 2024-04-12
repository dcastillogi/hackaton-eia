import clientPromise from "@/app/lib/mongodb";

export const POST = async (req: Request) => {
    const { name, telegram_id, chat_id} = await req.json();
    try {
        const client = await clientPromise;
        const db = client.db("main");
        const collection = db.collection("users");
        await collection.insertOne({ name, telegram_id });
        // send notification to telegram
        await fetch(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                chat_id: chat_id,
                text: `Bienvenido ${name} 😊. Ingresa el tema del que quieres escuchar un podcast:`,
            }),
        });
    } catch (error) {
        
    }
    return new Response(null, { status: 200 });

}