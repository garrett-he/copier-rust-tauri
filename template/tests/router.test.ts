import { describe, expect, it } from "vitest";
import router from "../src/router/index.ts";

describe("router", () => {
    it("creates router with home route", () => {
        expect(router).toBeDefined();
        expect(router.hasRoute("home")).toBe(true);
    });

    it("home route resolves to HomeView", () => {
        const route = router.resolve({ name: "home" });
        expect(route.name).toBe("home");
        expect(route.path).toBe("/");
    });
});
