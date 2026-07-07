import { useEffect, useState } from "react";
import {
  Alert,
  Button,
  Card,
  Flex,
  HStack,
  Heading,
  IconButton,
  Input,
  Spinner,
  Stack,
  Text,
} from "@chakra-ui/react";
import { LuTrash2 } from "react-icons/lu";
import { itemsApi, type Item } from "@/api/items";

export function ItemsPage() {
  const [items, setItems] = useState<Item[]>([]);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setItems(await itemsApi.list());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load items");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function handleCreate() {
    const trimmed = name.trim();
    if (!trimmed) return;
    try {
      await itemsApi.create({ name: trimmed });
      setName("");
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create item");
    }
  }

  async function handleDelete(id: number) {
    try {
      await itemsApi.remove(id);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to delete item");
    }
  }

  return (
    <Stack gap={6}>
      <Heading size="lg">Items</Heading>

      <HStack>
        <Input
          placeholder="New item name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleCreate()}
        />
        <Button onClick={handleCreate} disabled={!name.trim()}>
          Add
        </Button>
      </HStack>

      {error && (
        <Alert.Root status="error">
          <Alert.Indicator />
          <Alert.Title>{error}</Alert.Title>
        </Alert.Root>
      )}

      {loading ? (
        <Flex justify="center" py={8}>
          <Spinner />
        </Flex>
      ) : items.length === 0 ? (
        <Text color="fg.muted">No items yet. Add one above.</Text>
      ) : (
        <Stack gap={3}>
          {items.map((item) => (
            <Card.Root key={item.id}>
              <Card.Body>
                <Flex align="center">
                  <Stack gap={0}>
                    <Text fontWeight="medium">{item.name}</Text>
                    {item.description && (
                      <Text fontSize="sm" color="fg.muted">
                        {item.description}
                      </Text>
                    )}
                  </Stack>
                  <IconButton
                    aria-label="Delete item"
                    variant="ghost"
                    ml="auto"
                    onClick={() => handleDelete(item.id)}
                  >
                    <LuTrash2 />
                  </IconButton>
                </Flex>
              </Card.Body>
            </Card.Root>
          ))}
        </Stack>
      )}
    </Stack>
  );
}
