import { useState } from "react";
import { Badge, Box, Button, Flex, Heading, Icon, SimpleGrid, Stack, Text } from "@chakra-ui/react";
import {
  LuBuilding2,
  LuChevronDown,
  LuChevronUp,
  LuCircleCheck,
  LuFileText,
  LuPackage,
  LuTriangleAlert,
} from "react-icons/lu";
import type { EntitlementComparison } from "@/api/analysis";
import { SEVERITY } from "@/lib/severity";

function prettyConfig(raw: string): string {
  try {
    return JSON.stringify(JSON.parse(raw), null, 2);
  } catch {
    return raw;
  }
}

export function EntitlementCard({ item, index }: { item: EntitlementComparison; index: number }) {
  const [showTech, setShowTech] = useState(false);
  const [showSources, setShowSources] = useState(false);
  const sev = SEVERITY[item.deviation_severity] ?? SEVERITY.None;

  return (
    <Box
      borderWidth="1px"
      borderColor="blackAlpha.200"
      borderRadius="2xl"
      bg="white"
      overflow="hidden"
      boxShadow="0 1px 2px rgba(0,0,0,.04)"
    >
      {/* Accent stripe by severity */}
      <Box h="4px" bg={item.gap_detected ? sev.color : SEVERITY.None.color} />

      <Box px={{ base: 5, md: 7 }} py={5}>
        {/* Header */}
        <Flex justify="space-between" align="flex-start" gap={3} wrap="wrap" mb={4}>
          <Flex align="center" gap={3}>
            <Flex
              align="center"
              justify="center"
              w="32px"
              h="32px"
              borderRadius="full"
              bg="brand.subtle"
              color="marvel.700"
              fontFamily="heading"
              fontWeight="700"
              fontSize="sm"
              flexShrink={0}
            >
              {index + 1}
            </Flex>
            <Heading as="h3" fontSize="lg" fontFamily="heading">
              {item.area}
            </Heading>
          </Flex>
          <Flex gap={2} align="center">
            <Badge
              display="flex"
              alignItems="center"
              gap={1}
              bg={item.gap_detected ? sev.bg : SEVERITY.None.bg}
              color="black"
              borderRadius="full"
              px={3}
              py={1}
            >
              <Icon as={item.gap_detected ? LuTriangleAlert : LuCircleCheck} boxSize="14px" />
              {item.gap_detected ? "Afwijking" : "Sluit aan"}
            </Badge>
            {item.gap_detected && (
              <Badge bg={sev.color} color={sev.fg} borderRadius="full" px={3} py={1}>
                {sev.label} impact
              </Badge>
            )}
          </Flex>
        </Flex>

        {/* Current vs standard */}
        <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
          <Box bg="pastinaak" borderRadius="lg" p={4}>
            <Flex align="center" gap={2} mb={2}>
              <Icon as={LuBuilding2} color="marvel.700" boxSize="16px" />
              <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted">
                Huidige regeling van het fonds
              </Text>
            </Flex>
            <Text fontSize="sm">{item.current_entitlement_description}</Text>
          </Box>
          <Box bg="brand.subtle" borderRadius="lg" p={4}>
            <Flex align="center" gap={2} mb={2}>
              <Icon as={LuPackage} color="marvel.700" boxSize="16px" />
              <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted">
                Standaard Wtp-product
              </Text>
            </Flex>
            <Text fontSize="sm">{item.standard_offering_description}</Text>
          </Box>
        </SimpleGrid>

        {/* What it means */}
        <Box mt={4} borderLeftWidth="3px" borderColor={sev.color} pl={4} py={1}>
          <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted" mb={1}>
            Wat betekent dit?
          </Text>
          <Text fontSize="sm">{item.actuarial_implication}</Text>
        </Box>

        {/* Collapsible: technical config + sources */}
        <Flex mt={4} gap={4} wrap="wrap">
          <Button size="xs" variant="ghost" color="marvel.700" onClick={() => setShowTech((s) => !s)}>
            <Icon as={showTech ? LuChevronUp : LuChevronDown} />
            Technische vertaling (Qwik)
          </Button>
          {item.sources.length > 0 && (
            <Button
              size="xs"
              variant="ghost"
              color="marvel.700"
              onClick={() => setShowSources((s) => !s)}
            >
              <Icon as={showSources ? LuChevronUp : LuChevronDown} />
              Bronnen ({item.sources.length})
            </Button>
          )}
        </Flex>

        {showTech && (
          <Box
            as="pre"
            mt={2}
            fontFamily="mono"
            fontSize="xs"
            bg="#0B4E71"
            color="#EAF7FF"
            p={4}
            borderRadius="md"
            overflowX="auto"
            whiteSpace="pre"
          >
            {prettyConfig(item.required_qwik_configuration)}
          </Box>
        )}

        {showSources && item.sources.length > 0 && (
          <Stack gap={2} mt={2}>
            {item.sources.map((src, i) => (
              <Flex key={i} gap={3} bg="pastinaak" borderRadius="md" px={4} py={3}>
                <Icon as={LuFileText} color="marvel.700" boxSize="16px" mt="2px" flexShrink={0} />
                <Box>
                  <Text fontSize="xs" fontWeight="700">
                    {src.document_name} — {src.section}{" "}
                    <Text as="span" color="fg.muted" fontWeight="400">
                      (pagina {src.page_number})
                    </Text>
                  </Text>
                  <Text fontSize="xs" color="fg.muted" fontStyle="italic">
                    “{src.quote}”
                  </Text>
                </Box>
              </Flex>
            ))}
          </Stack>
        )}
      </Box>
    </Box>
  );
}
