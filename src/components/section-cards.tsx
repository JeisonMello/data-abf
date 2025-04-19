"use client";

export function SectionCards() {
  const cards = [
    { title: "Sales", value: "$24,000", change: "+12%" },
    { title: "Users", value: "1,200", change: "+5%" },
    { title: "Orders", value: "320", change: "-2%" },
    { title: "Revenue", value: "$8,000", change: "+8%" },
  ];

  return (
    <div className="grid gap-4 px-4 sm:grid-cols-2 lg:grid-cols-4 lg:px-6">
      {cards.map((card, index) => (
        <div
          key={index}
          className="rounded-lg border bg-white p-4 shadow-sm hover:shadow-md transition-shadow"
        >
          <div className="text-sm font-medium text-gray-500">{card.title}</div>
          <div className="mt-1 text-xl font-semibold text-gray-900">
            {card.value}
          </div>
          <div
            className={`mt-1 text-sm ${
              card.change.startsWith("+") ? "text-green-500" : "text-red-500"
            }`}
          >
            {card.change}
          </div>
        </div>
      ))}
    </div>
  );
}
