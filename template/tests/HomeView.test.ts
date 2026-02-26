import { mount } from "@vue/test-utils";
import { describe, expect, it, vi } from "vitest";
import HomeView from "../src/views/HomeView.vue";

vi.mock("@tauri-apps/api/core", () => ({
    invoke: vi.fn(),
}));

import { invoke } from "@tauri-apps/api/core";

const mockedInvoke = vi.mocked(invoke);

describe("HomeView", () => {
    it("renders title and form elements", () => {
        const wrapper = mount(HomeView);

        expect(wrapper.find("h1").text()).toBe("Welcome to Tauri + Vue");
        expect(wrapper.find("input#greet-input").exists()).toBe(true);
        expect(wrapper.find("button[type='submit']").exists()).toBe(true);
    });

    it("updates name on input", async () => {
        const wrapper = mount(HomeView);
        const input = wrapper.find("input#greet-input");

        await input.setValue("Alice");

        expect(input.element.value).toBe("Alice");
    });

    it("calls invoke on form submit and displays greeting", async () => {
        mockedInvoke.mockResolvedValueOnce("Hello, Bob! You've been greeted from Rust!");

        const wrapper = mount(HomeView);
        const input = wrapper.find("input#greet-input");
        const form = wrapper.find("form");

        await input.setValue("Bob");
        await form.trigger("submit");

        expect(mockedInvoke).toHaveBeenCalledWith("greet", { name: "Bob" });
        expect(mockedInvoke).toHaveBeenCalledTimes(1);

        await wrapper.vm.$nextTick();
        expect(wrapper.text()).toContain("Hello, Bob! You've been greeted from Rust!");
    });

    it("displays empty greeting initially", () => {
        const wrapper = mount(HomeView);
        expect(wrapper.text()).not.toContain("You've been greeted from Rust");
    });
});
