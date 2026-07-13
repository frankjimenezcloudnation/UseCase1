import { Badge, Box, Button, Flex, Heading, Icon, Stack, Text } from "@chakra-ui/react";
import { LuFileText, LuTriangleAlert, LuX } from "react-icons/lu";
import type { DocumentInfo } from "@/api/analysis";

export interface DuplicateConflict {
  side: "fund" | "benchmark";
  docType: string;
  docs: DocumentInfo[];
}

interface Props {
  conflicts: DuplicateConflict[];
  onClose: () => void;
}

const SIDE_LABEL: Record<"fund" | "benchmark", string> = {
  fund: "Documenten van het fonds",
  benchmark: "Standaardproduct",
};

export function DuplicateWarningDialog({ conflicts, onClose }: Props) {
  return (
    <Box
      position="fixed"
      inset={0}
      bg="blackAlpha.600"
      zIndex={1400}
      display="flex"
      alignItems="center"
      justifyContent="center"
      p={4}
      onClick={onClose}
    >
      <Box
        bg="white"
        borderRadius="2xl"
        maxW="lg"
        w="100%"
        boxShadow="0 20px 60px rgba(0,0,0,.25)"
        overflow="hidden"
        onClick={(e) => e.stopPropagation()}
        role="alertdialog"
        aria-modal="true"
      >
        <Box h="4px" bg="#E8920C" />
        <Box p={{ base: 5, md: 7 }}>
          <Flex justify="space-between" align="flex-start" gap={3} mb={2}>
            <Flex align="center" gap={3}>
              <Flex
                align="center"
                justify="center"
                w="36px"
                h="36px"
                borderRadius="full"
                bg="#FDF1DD"
                flexShrink={0}
              >
                <Icon as={LuTriangleAlert} color="#E8920C" boxSize="20px" />
              </Flex>
              <Heading as="h2" fontSize="xl" fontFamily="heading">
                Dubbele documenten geselecteerd
              </Heading>
            </Flex>
            <Button size="xs" variant="ghost" onClick={onClose} aria-label="Sluiten">
              <Icon as={LuX} />
            </Button>
          </Flex>

          <Text fontSize="sm" color="fg.muted" mb={4}>
            U heeft meerdere documenten van hetzelfde type aangevinkt. Als er twee documenten van
            hetzelfde soort naast elkaar staan, kunnen ze door elkaar gaan lopen en wordt de
            vergelijking onbetrouwbaar. Vink per type één document aan; de vergelijking kan pas
            starten als elk type uniek is.
          </Text>

          <Stack gap={4} mb={5}>
            {conflicts.map((c) => (
              <Box key={`${c.side}-${c.docType}`} borderWidth="1px" borderColor="blackAlpha.200" borderRadius="lg" p={4}>
                <Flex align="center" gap={2} mb={2} wrap="wrap">
                  <Badge bg="#FDF1DD" color="#8A5A00" borderRadius="full" px={3} py={1}>
                    {c.docType}
                  </Badge>
                  <Text fontSize="xs" color="fg.muted">
                    · {SIDE_LABEL[c.side]} · {c.docs.length}× aangevinkt
                  </Text>
                </Flex>
                <Stack gap={1}>
                  {c.docs.map((d) => (
                    <Flex key={d.id} align="center" gap={2}>
                      <Icon as={LuFileText} color="fg.muted" boxSize="14px" flexShrink={0} />
                      <Text fontSize="sm" lineClamp={1}>
                        {d.filename}
                      </Text>
                    </Flex>
                  ))}
                </Stack>
              </Box>
            ))}
          </Stack>

          <Flex justify="flex-end">
            <Button
              bg="marvel.400"
              color="black"
              fontWeight="700"
              borderRadius="full"
              px={6}
              _hover={{ bg: "marvel.500" }}
              onClick={onClose}
            >
              Selectie aanpassen
            </Button>
          </Flex>
        </Box>
      </Box>
    </Box>
  );
}
