"use client";

import * as React from "react";

type DataItem = {
  name: string;
  status: string;
  value: number;
};

export function DataTable({ data }: { data: DataItem[] }) {
  return (
    <div className="px-4 lg:px-6">
      <div className="overflow-auto rounded-lg border border-gray-200 shadow-sm">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50 text-gray-600 font-medium">
            <tr>
              <th className="px-4 py-2 text-left">Name</th>
              <th className="px-4 py-2 text-left">Status</th>
              <th className="px-4 py-2 text-left">Value</th>
            </tr>
          </thead>
          <tbody className="text-gray-800">
            {data.map((item, index) => (
              <tr
                key={index}
                className="border-t hover:bg-gray-50 transition-colors"
              >
                <td className="px-4 py-2">{item.name}</td>
                <td className="px-4 py-2">{item.status}</td>
                <td className="px-4 py-2">{item.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
