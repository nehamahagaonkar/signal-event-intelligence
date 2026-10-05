"use client";

import { useEffect, useState } from "react";

const API =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";
type Lead = {
  id: number;
  name: string;
  company_id: number;
  email: string;
  event_id: number;
  notes: string | null;
  follow_up_status: string;
  created_at: string;
  updated_at: string;
};

type Company = {
  id: number;
  name: string;
};

type Event = {
  id: number;
  title: string;
};

const statusOptions = [
  "pending",
  "contacted",
  "followed_up",
  "converted",
];

export default function Home() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [events, setEvents] = useState<Event[]>([]);

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [editingLead, setEditingLead] = useState<Lead | null>(null);

  const [form, setForm] = useState({
    name: "",
    company_id: "",
    email: "",
    event_id: "",
    notes: "",
    follow_up_status: "pending",
  });

  const [loading, setLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState<{
  leadId: number;
  type: "summary" | "follow-up";
} | null>(null);
  const [aiResult, setAiResult] = useState<{
    type: "summary" | "follow-up";
    leadId: number;
    text: string;
  } | null>(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    loadLeads();
  }, [search, statusFilter]);

  async function loadInitialData() {
    try {
      const [companiesRes, eventsRes] = await Promise.all([
        fetch(`${API}/companies/`),
        fetch(`${API}/events/`),
      ]);

      const companiesData = await companiesRes.json();
      const eventsData = await eventsRes.json();

      setCompanies(companiesData);
      setEvents(eventsData);
    } catch (error) {
      console.error("Failed to load initial data:", error);
    }
  }

  async function loadLeads() {
    try {
      const params = new URLSearchParams();

      if (search) params.append("search", search);
      if (statusFilter) {
        params.append("follow_up_status", statusFilter);
      }

      const response = await fetch(
        `${API}/leads/?${params.toString()}`
      );

      const data = await response.json();

      setLeads(data);
      setLoading(false);
    } catch (error) {
      console.error("Failed to load leads:", error);
      setLoading(false);
    }
  }

  function openCreateForm() {
    setEditingLead(null);

    setForm({
      name: "",
      company_id: companies[0]?.id?.toString() || "",
      email: "",
      event_id: events[0]?.id?.toString() || "",
      notes: "",
      follow_up_status: "pending",
    });

    setShowForm(true);
  }

  function openEditForm(lead: Lead) {
    setEditingLead(lead);

    setForm({
      name: lead.name,
      company_id: lead.company_id.toString(),
      email: lead.email,
      event_id: lead.event_id.toString(),
      notes: lead.notes || "",
      follow_up_status: lead.follow_up_status,
    });

    setShowForm(true);
  }

  async function saveLead(e: React.FormEvent) {
    e.preventDefault();

    const payload = {
      name: form.name,
      company_id: Number(form.company_id),
      email: form.email,
      event_id: Number(form.event_id),
      notes: form.notes,
      follow_up_status: form.follow_up_status,
    };

    try {
      const url = editingLead
        ? `${API}/leads/${editingLead.id}`
        : `${API}/leads/`;

      const method = editingLead ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const error = await response.json();
        alert(error.detail || "Failed to save lead");
        return;
      }

      setShowForm(false);
      setEditingLead(null);

      await loadLeads();
    } catch (error) {
      console.error("Failed to save lead:", error);
    }
  }

  async function deleteLead(id: number) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this lead?"
    );

    if (!confirmed) return;

    try {
      const response = await fetch(`${API}/leads/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        await loadLeads();
      }
    } catch (error) {
      console.error("Failed to delete lead:", error);
    }
  }

  async function generateAI(
  leadId: number,
  type: "summary" | "follow-up"
) {
  setAiLoading({
  leadId,
  type,
});

  setAiResult(null);

  try {
    const endpoint =
      type === "summary"
        ? `${API}/ai/leads/${leadId}/summary`
        : `${API}/ai/leads/${leadId}/follow-up`;

    const response = await fetch(endpoint, {
      method: "POST",
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "AI generation failed");
      return;
    }

    setAiResult({
      type,
      leadId,
      text:
        type === "summary"
          ? data.summary
          : data.follow_up,
    });
  } catch (error) {
    console.error("AI request failed:", error);

    alert(
      "Could not connect to the AI service. Make sure Ollama is running."
    );
  } finally {
    setAiLoading(null);
  }
}

  function getCompanyName(companyId: number) {
    return (
      companies.find(
        (company) => company.id === companyId
      )?.name || `Company #${companyId}`
    );
  }

  function getEventName(eventId: number) {
    return (
      events.find(
        (event) => event.id === eventId
      )?.title || `Event #${eventId}`
    );
  }

  function getStatusStyle(status: string) {
    switch (status) {
      case "converted":
        return "bg-emerald-50 text-emerald-700 border-emerald-200";

      case "contacted":
        return "bg-blue-50 text-blue-700 border-blue-200";

      case "followed_up":
        return "bg-violet-50 text-violet-700 border-violet-200";

      default:
        return "bg-amber-50 text-amber-700 border-amber-200";
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-7xl px-6 py-7 md:px-8">
          <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs font-semibold tracking-[0.18em] text-blue-600">
                SIGNAL INTELLIGENCE
              </p>

              <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
                Event Lead Manager
              </h1>

              <p className="mt-2 max-w-xl text-sm text-slate-500">
                Manage event contacts, track follow-ups, and use AI
                to turn conversations into actionable next steps.
              </p>
            </div>

            <button
              onClick={openCreateForm}
              className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700"
            >
              + Add Lead
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8 md:px-8">
        {/* Stats */}
        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-slate-500">Total Leads</p>
            <p className="mt-2 text-3xl font-bold text-slate-900">
              {leads.length}
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-slate-500">Pending</p>
            <p className="mt-2 text-3xl font-bold text-amber-600">
              {
                leads.filter(
                  (lead) =>
                    lead.follow_up_status === "pending"
                ).length
              }
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-slate-500">Contacted</p>
            <p className="mt-2 text-3xl font-bold text-blue-600">
              {
                leads.filter(
                  (lead) =>
                    lead.follow_up_status === "contacted"
                ).length
              }
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-slate-500">Converted</p>
            <p className="mt-2 text-3xl font-bold text-emerald-600">
              {
                leads.filter(
                  (lead) =>
                    lead.follow_up_status === "converted"
                ).length
              }
            </p>
          </div>
        </section>

        {/* Leads */}
        <section className="mt-8">
          <div className="mb-5 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-900">
                Event Leads
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Contacts captured from events and networking
                interactions.
              </p>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row">
              <input
                type="text"
                placeholder="Search name or email..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none placeholder:text-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 sm:w-64"
              />

              <select
                value={statusFilter}
                onChange={(e) =>
                  setStatusFilter(e.target.value)
                }
                className="rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm capitalize text-slate-700 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              >
                <option value="">All statuses</option>

                {statusOptions.map((status) => (
                  <option key={status} value={status}>
                    {status.replace("_", " ")}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-slate-200 bg-slate-50">
                  <tr>
                    <th className="px-5 py-4 font-semibold text-slate-500">
                      Lead
                    </th>

                    <th className="px-5 py-4 font-semibold text-slate-500">
                      Company
                    </th>

                    <th className="px-5 py-4 font-semibold text-slate-500">
                      Event
                    </th>

                    <th className="px-5 py-4 font-semibold text-slate-500">
                      Status
                    </th>

                    <th className="px-5 py-4 font-semibold text-slate-500">
                      Notes
                    </th>

                    <th className="px-5 py-4 text-right font-semibold text-slate-500">
                      Actions
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {loading ? (
                    <tr>
                      <td
                        colSpan={6}
                        className="px-5 py-12 text-center text-slate-400"
                      >
                        Loading leads...
                      </td>
                    </tr>
                  ) : leads.length === 0 ? (
                    <tr>
                      <td
                        colSpan={6}
                        className="px-5 py-12 text-center text-slate-400"
                      >
                        No leads found.
                      </td>
                    </tr>
                  ) : (
                    leads.map((lead) => (
                      <tr
                        key={lead.id}
                        className="border-b border-slate-100 last:border-0 hover:bg-slate-50"
                      >
                        <td className="px-5 py-4">
                          <div className="font-semibold text-slate-900">
                            {lead.name}
                          </div>

                          <div className="mt-1 text-xs text-slate-500">
                            {lead.email}
                          </div>
                        </td>

                        <td className="px-5 py-4 text-slate-700">
                          {getCompanyName(lead.company_id)}
                        </td>

                        <td className="max-w-xs px-5 py-4 text-slate-700">
                          {getEventName(lead.event_id)}
                        </td>

                        <td className="px-5 py-4">
                          <span
                            className={`inline-flex rounded-full border px-3 py-1 text-xs font-medium capitalize ${getStatusStyle(
                              lead.follow_up_status
                            )}`}
                          >
                            {lead.follow_up_status.replace(
                              "_",
                              " "
                            )}
                          </span>
                        </td>

                        <td className="max-w-xs px-5 py-4 text-slate-500">
                          <p className="truncate">
                            {lead.notes || "—"}
                          </p>
                        </td>

                        <td className="px-5 py-4">
                          <div className="flex flex-wrap justify-end gap-2">
                            <button
                              onClick={() =>
                                generateAI(
                                  lead.id,
                                  "summary"
                                )
                              }
                              disabled={
                                aiLoading?.leadId=== lead.id
                              }
                              className="rounded-md border border-violet-200 bg-violet-50 px-3 py-1.5 text-xs font-medium text-violet-700 transition hover:bg-violet-100 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                              {aiLoading?.leadId === lead.id &&
aiLoading?.type === "summary"
  ? "Generating..."
  : "AI Summary"}
                            </button>

                            <button
                              onClick={() =>
                                generateAI(
                                  lead.id,
                                  "follow-up"
                                )
                              }
                              disabled={
                                aiLoading?.leadId === lead.id
                              }
                              className="rounded-md border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-700 transition hover:bg-blue-100 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                              AI Follow-up
                            </button>

                            <button
                              onClick={() =>
                                openEditForm(lead)
                              }
                              className="rounded-md border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:bg-slate-100"
                            >
                              Edit
                            </button>

                            <button
                              onClick={() =>
                                deleteLead(lead.id)
                              }
                              className="rounded-md border border-red-200 bg-white px-3 py-1.5 text-xs font-medium text-red-600 transition hover:bg-red-50"
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>

      {/* AI Modal */}
      {/* AI Loading Modal */}
{aiLoading && (
  <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-sm">
    <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-7 text-center shadow-2xl">
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-blue-50">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-blue-200 border-t-blue-600" />
      </div>

      <h2 className="mt-5 text-lg font-bold text-slate-900">
        {aiLoading.type === "summary"
          ? "Generating AI summary..."
          : "Drafting follow-up..."}
      </h2>

      <p className="mt-2 text-sm leading-6 text-slate-500">
        AI is processing the interaction notes.
        This may take a few seconds.
      </p>
    </div>
  </div>
)}

      {/* Add/Edit Lead Modal */}
      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-sm">
          <div className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl">
            <div className="mb-6 flex items-start justify-between">
              <div>
                <h2 className="text-xl font-bold text-slate-900">
                  {editingLead ? "Edit Lead" : "Add Lead"}
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Capture event contact information.
                </p>
              </div>

              <button
                onClick={() => setShowForm(false)}
                className="rounded-md px-2 text-2xl leading-none text-slate-400 hover:bg-slate-100 hover:text-slate-700"
              >
                ×
              </button>
            </div>

            <form onSubmit={saveLead} className="space-y-4">
              <div>
                <label className="mb-1.5 block text-sm font-medium text-slate-700">
                  Name
                </label>

                <input
                  required
                  value={form.name}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      name: e.target.value,
                    })
                  }
                  className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  placeholder="Contact name"
                />
              </div>

              <div>
                <label className="mb-1.5 block text-sm font-medium text-slate-700">
                  Email
                </label>

                <input
                  required
                  type="email"
                  value={form.email}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      email: e.target.value,
                    })
                  }
                  className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  placeholder="contact@company.com"
                />
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="mb-1.5 block text-sm font-medium text-slate-700">
                    Company
                  </label>

                  <select
                    required
                    value={form.company_id}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        company_id: e.target.value,
                      })
                    }
                    className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  >
                    <option value="">
                      Select company
                    </option>

                    {companies.map((company) => (
                      <option
                        key={company.id}
                        value={company.id}
                      >
                        {company.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="mb-1.5 block text-sm font-medium text-slate-700">
                    Event
                  </label>

                  <select
                    required
                    value={form.event_id}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        event_id: e.target.value,
                      })
                    }
                    className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  >
                    <option value="">
                      Select event
                    </option>

                    {events.map((event) => (
                      <option
                        key={event.id}
                        value={event.id}
                      >
                        {event.title}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="mb-1.5 block text-sm font-medium text-slate-700">
                  Follow-up Status
                </label>

                <select
                  value={form.follow_up_status}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      follow_up_status: e.target.value,
                    })
                  }
                  className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm capitalize text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                >
                  {statusOptions.map((status) => (
                    <option key={status} value={status}>
                      {status.replace("_", " ")}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="mb-1.5 block text-sm font-medium text-slate-700">
                  Interaction Notes
                </label>

                <textarea
                  rows={4}
                  value={form.notes}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      notes: e.target.value,
                    })
                  }
                  className="w-full resize-none rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  placeholder="What did you discuss with this lead?"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="rounded-lg border border-slate-300 bg-white px-5 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700"
                >
                  {editingLead
                    ? "Save Changes"
                    : "Create Lead"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}