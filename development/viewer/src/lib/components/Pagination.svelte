<script lang="ts">
  import { Button } from "$lib/components/ui/button";

  let {
    itemLabel,
    page,
    pageCount,
    pageSize,
    placement,
    total,
    onSelect,
  }: {
    itemLabel: string;
    page: number;
    pageCount: number;
    pageSize: number;
    placement: "top" | "bottom";
    total: number;
    onSelect: (page: number) => void;
  } = $props();

</script>

<nav class="pagination pagination-{placement}" aria-label={`${itemLabel} pages, ${placement}`}>
  <span>{(page - 1) * pageSize + 1}–{Math.min(page * pageSize, total)} of {total}</span>
  <Button size="sm" variant="outline" aria-label={`Previous ${itemLabel} page`} disabled={page === 1} onclick={() => onSelect(page - 1)}>Previous</Button>
  <span aria-live={placement === "bottom" ? "polite" : undefined} aria-atomic={placement === "bottom" ? "true" : undefined}>Page {page} of {pageCount}</span>
  <Button size="sm" variant="outline" aria-label={`Next ${itemLabel} page`} disabled={page === pageCount} onclick={() => onSelect(page + 1)}>Next</Button>
</nav>
