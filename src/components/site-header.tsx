"use client";

import { Menu } from "lucide-react";

import { SidebarTrigger } from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";

export function SiteHeader() {
  return (
    <header className="flex h-14 items-center gap-4 border-b bg-background px-6">
      <SidebarTrigger>
        <Menu className="h-6 w-6" />
      </SidebarTrigger>
      <div className="text-lg font-semibold">Dashboard</div>
      <div className="ml-auto flex items-center space-x-4">
        <Button variant="outline" size="sm">
          Settings
        </Button>
      </div>
    </header>
  );
}
