"use client";

import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [tasks, setTasks] = useState<any[]>([]);

  async function unmess() {
    if (!text.trim()) return;

  setLoading(true);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/brain-dump",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
        }),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();

      throw new Error(
        `Backend error ${response.status}: ${errorText}`
      );
    }

    const data = await response.json();

    console.log("Backend response:", data);

    setTasks(data.tasks ?? []);

  } catch (error) {

    console.error("UNMESS ERROR:", error);

    alert(
      "Could not connect to the Unmess backend. " +
      "Make sure FastAPI is running on port 8000."
    );

  } finally {
    setLoading(false);
  }
}
  

  return (
    <main className="min-h-screen bg-zinc-950 text-white p-10">
      <div className="max-w-4xl mx-auto">

        <h1 className="text-5xl font-bold mb-4">
          Unmessss.
        </h1>

        <p className="text-zinc-400 mb-10">
          Turn the chaos in your head into a plan.
        </p>

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="What's on your mind?"
          className="w-full h-48 rounded-2xl bg-zinc-900 border border-zinc-800 p-5 outline-none"
        />

        <button
          onClick={unmess}
          className="mt-5 px-6 py-3 rounded-xl bg-white text-black font-semibold"
        >
          {loading ? "Unmessing..." : "✦ Unmess it"}
        </button>

        <div className="mt-10 space-y-4">

          {tasks.map((task, index) => (

            <div
              key={task.id ?? `${task.title}-${index}`}
              className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5"
            >
             <div className="flex justify-between">
              <h2 className="font-semibold text-lg">
                {task.title || "Untitled task"}
              </h2>

              <span className="text-sm text-zinc-400">
                {task.priority || "normal"}
              </span>
            </div>


           {task.deadline && (
            <p className="text-sm text-zinc-400 mt-2">
              Deadline: {task.deadline}
            </p>
          )}

          {task.blocker && (
            <p className="text-sm text-red-400 mt-2">
              Blocked by: {task.blocker}
            </p>
          )}

          {task.description && (
            <p className="text-sm text-zinc-500 mt-2">
              {task.description}
            </p>
        )}
      </div>
    ))}

        </div>

      </div>
    </main>
  );
}
