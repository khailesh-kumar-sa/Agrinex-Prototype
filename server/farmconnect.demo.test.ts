import { describe, expect, it } from "vitest";
import { canAccess, products, roleAccess } from "../client/src/App";

describe("FarmConnect demo catalog", () => {
  it("ships the 12 core produce listings requested for judge mode", () => {
    expect(products).toHaveLength(12);
    expect(products.map(product => product.name)).toEqual(expect.arrayContaining([
      "Tomatoes",
      "Potatoes",
      "Onions",
      "Basmati Rice",
      "Wheat",
      "Alphonso Mangoes",
      "Himachal Apples",
      "Chickpeas",
      "Groundnuts",
      "Robusta Bananas",
      "Brinjal",
      "Green Chillies",
    ]));
  });

  it("contains the seeded tomato scenario used in the order flow", () => {
    const tomatoes = products.find(product => product.id === "tomatoes");
    expect(tomatoes).toMatchObject({
      farmer: "Arun Kumar",
      location: "Nashik, MH",
      qty: 100,
      price: 30,
      rating: 4.9,
      organic: true,
    });
  });
});

describe("FarmConnect demo role access", () => {
  it("gives each demo role an explicit access profile", () => {
    expect(Object.keys(roleAccess)).toEqual([
      "Consumer Demo",
      "Farmer Demo",
      "FPO Demo",
      "Bulk Buyer Demo",
      "Admin Demo",
    ]);
    expect(canAccess("Consumer Demo", "/marketplace")).toBe(true);
    expect(canAccess("Consumer Demo", "/admin")).toBe(false);
    expect(canAccess("Farmer Demo", "/inventory")).toBe(true);
    expect(canAccess("Farmer Demo", "/bulk-buyers")).toBe(false);
    expect(canAccess("FPO Demo", "/bulk-buyers")).toBe(true);
    expect(canAccess("Bulk Buyer Demo", "/payments")).toBe(true);
    expect(canAccess("Admin Demo", "/admin")).toBe(true);
  });

  it("treats product detail pages as belonging to the marketplace capability", () => {
    expect(canAccess("Consumer Demo", "/product/tomatoes")).toBe(true);
    expect(canAccess("Farmer Demo", "/product/onions")).toBe(true);
  });
});
