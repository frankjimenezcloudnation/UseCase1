import { useRef, useState } from "react";
import { Box, Button, Flex, Icon, Input, Stack, Text } from "@chakra-ui/react";
import {
  LuCheck,
  LuFileText,
  LuGripVertical,
  LuPencil,
  LuPlus,
  LuTrash2,
  LuX,
} from "react-icons/lu";
import type { DocumentInfo } from "@/api/analysis";

interface Props {
  title: string;
  role: "fund" | "benchmark";
  documents: DocumentInfo[];
  selected: Set<string>;
  busy: boolean;
  onToggle: (id: string) => void;
  onUpload: (file: File, role: "fund" | "benchmark") => void;
  onDelete: (id: string) => void;
  onEdit: (id: string, patch: { role?: "fund" | "benchmark"; doc_type?: string }) => void;
  onReorder: (orderedIds: string[]) => void;
}

export function DocumentSelector({
  title,
  role,
  documents,
  selected,
  busy,
  onToggle,
  onUpload,
  onDelete,
  onEdit,
  onReorder,
}: Props) {
  const fileRef = useRef<HTMLInputElement>(null);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [draftLabel, setDraftLabel] = useState("");
  const [draftRole, setDraftRole] = useState<"fund" | "benchmark">(role);
  const [dragId, setDragId] = useState<string | null>(null);

  function startEdit(doc: DocumentInfo) {
    setEditingId(doc.id);
    setDraftLabel(doc.doc_type);
    setDraftRole(doc.role);
  }

  function saveEdit(doc: DocumentInfo) {
    const patch: { role?: "fund" | "benchmark"; doc_type?: string } = {};
    if (draftLabel.trim() && draftLabel.trim() !== doc.doc_type) patch.doc_type = draftLabel.trim();
    if (draftRole !== doc.role) patch.role = draftRole;
    if (patch.role || patch.doc_type) onEdit(doc.id, patch);
    setEditingId(null);
  }

  function handleDrop(targetId: string) {
    if (!dragId || dragId === targetId) return setDragId(null);
    const ids = documents.map((d) => d.id);
    const from = ids.indexOf(dragId);
    const to = ids.indexOf(targetId);
    if (from < 0 || to < 0) return setDragId(null);
    ids.splice(to, 0, ids.splice(from, 1)[0]);
    onReorder(ids);
    setDragId(null);
  }

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={3} gap={2}>
        <Text
          fontFamily="heading"
          fontWeight="700"
          fontSize="sm"
          textTransform="uppercase"
          letterSpacing="0.08em"
          color="fg.muted"
        >
          {title}
        </Text>
        <Button
          size="xs"
          variant="outline"
          borderRadius="full"
          onClick={() => fileRef.current?.click()}
          disabled={busy}
        >
          <Icon as={LuPlus} /> Toevoegen
        </Button>
        <input
          ref={fileRef}
          type="file"
          accept=".pdf,.docx,.xlsx,.xls"
          style={{ display: "none" }}
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) onUpload(f, role);
            e.target.value = "";
          }}
        />
      </Flex>

      <Stack gap={2}>
        {documents.length === 0 && (
          <Text fontSize="sm" color="fg.muted" fontStyle="italic">
            Nog geen documenten. Gebruik “Toevoegen” om er een te uploaden.
          </Text>
        )}
        {documents.map((doc) => {
          const isSelected = selected.has(doc.id);
          const isEditing = editingId === doc.id;
          return (
            <Box
              key={doc.id}
              borderWidth="1px"
              borderColor={isSelected ? "marvel.400" : "blackAlpha.200"}
              bg={isSelected ? "brand.subtle" : "white"}
              borderRadius="lg"
              opacity={dragId === doc.id ? 0.5 : 1}
              transition="all 0.15s"
              draggable={!isEditing}
              onDragStart={() => setDragId(doc.id)}
              onDragOver={(e) => e.preventDefault()}
              onDrop={() => handleDrop(doc.id)}
              onDragEnd={() => setDragId(null)}
            >
              {isEditing ? (
                <Stack gap={3} p={4}>
                  <Input
                    size="sm"
                    value={draftLabel}
                    onChange={(e) => setDraftLabel(e.target.value)}
                    placeholder="Naam / type-label"
                  />
                  <Flex gap={2} align="center" wrap="wrap">
                    <Text fontSize="xs" color="fg.muted">
                      Rol:
                    </Text>
                    {(["fund", "benchmark"] as const).map((r) => (
                      <Button
                        key={r}
                        size="xs"
                        variant={draftRole === r ? "solid" : "outline"}
                        bg={draftRole === r ? "marvel.400" : undefined}
                        color={draftRole === r ? "black" : undefined}
                        borderRadius="full"
                        onClick={() => setDraftRole(r)}
                      >
                        {r === "fund" ? "Fonds" : "Standaard"}
                      </Button>
                    ))}
                    <Flex gap={2} ml="auto">
                      <Button size="xs" variant="ghost" onClick={() => setEditingId(null)}>
                        <Icon as={LuX} /> Annuleren
                      </Button>
                      <Button
                        size="xs"
                        bg="marvel.400"
                        color="black"
                        borderRadius="full"
                        onClick={() => saveEdit(doc)}
                      >
                        <Icon as={LuCheck} /> Opslaan
                      </Button>
                    </Flex>
                  </Flex>
                </Stack>
              ) : (
                <Flex align="center" gap={2} px={3} py={3}>
                  <Icon as={LuGripVertical} color="blackAlpha.400" boxSize="16px" cursor="grab" flexShrink={0} />
                  <Flex
                    align="center"
                    justify="center"
                    w="20px"
                    h="20px"
                    borderRadius="sm"
                    borderWidth="2px"
                    borderColor={isSelected ? "marvel.400" : "blackAlpha.400"}
                    bg={isSelected ? "marvel.400" : "transparent"}
                    flexShrink={0}
                    cursor="pointer"
                    onClick={() => onToggle(doc.id)}
                  >
                    {isSelected && <Icon as={LuCheck} color="black" boxSize="14px" />}
                  </Flex>
                  <Icon as={LuFileText} color="fg.muted" boxSize="18px" flexShrink={0} />
                  <Box minW={0} flex={1} cursor="pointer" onClick={() => onToggle(doc.id)}>
                    <Flex align="center" gap={2}>
                      <Text fontWeight="600" fontSize="sm" lineClamp={1}>
                        {doc.doc_type}
                      </Text>
                      {doc.source === "upload" && (
                        <Box fontSize="2xs" bg="mintgroen" color="black" borderRadius="full" px={2} py="1px">
                          geüpload
                        </Box>
                      )}
                    </Flex>
                    <Text fontSize="xs" color="fg.muted" lineClamp={1}>
                      {doc.filename}
                    </Text>
                  </Box>
                  <Button size="xs" variant="ghost" onClick={() => startEdit(doc)} disabled={busy} title="Wijzigen">
                    <Icon as={LuPencil} boxSize="14px" />
                  </Button>
                  <Button
                    size="xs"
                    variant="ghost"
                    color="#C0392B"
                    onClick={() => onDelete(doc.id)}
                    disabled={busy}
                    title={doc.source === "upload" ? "Verwijderen" : "Verbergen"}
                  >
                    <Icon as={LuTrash2} boxSize="14px" />
                  </Button>
                </Flex>
              )}
            </Box>
          );
        })}
      </Stack>
    </Box>
  );
}
