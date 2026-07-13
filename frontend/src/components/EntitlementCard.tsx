import { useState } from "react";
import { Badge, Box, Button, Flex, Heading, Icon, SimpleGrid, Stack, Text } from "@chakra-ui/react";
import {
  LuBuilding2,
  LuChevronDown,
  LuChevronUp,
  LuCircleCheck,
  LuPackage,
  LuShieldCheck,
  LuShieldAlert,
  LuTriangleAlert,
} from "react-icons/lu";
import type { EntitlementComparison, EvidenceLevel, ProvisionSource } from "@/api/analysis";
import { SEVERITY } from "@/lib/severity";

const EVIDENCE: Record<EvidenceLevel, { bg: string; fg: string; label: string }> = {
  Hoog: { bg: "#E4F6EC", fg: "#1E7A50", label: "Sterk onderbouwd" },
  Middel: { bg: "#FDF1DD", fg: "#8A5A00", label: "Redelijk onderbouwd" },
  Laag: { bg: "#FEECE8", fg: "#B23A2A", label: "Zwak onderbouwd" },
};

/** Belt-and-suspenders: strip any stray LaTeX/math so nothing like "$A=\sum..." ever renders. */
function plain(raw: string): string {
  if (!raw) return "";
  return raw
    .replace(/\$[^$]*\$/g, "") // inline math
    .replace(/\\[a-zA-Z]+/g, "") // \sum, \cdot, \frac, ...
    .replace(/[{}$_^]/g, "")
    .replace(/\s{2,}/g, " ")
    .trim();
}

function prettyConfig(raw: string): string {
  try {
    return JSON.stringify(JSON.parse(raw), null, 2);
  } catch {
    return raw;
  }
}

function BulletList({ items, color }: { items: string[]; color: string }) {
  if (!items?.length) {
    return (
      <Text fontSize="sm" color="fg.muted" fontStyle="italic">
        Niet vermeld in de documenten.
      </Text>
    );
  }
  return (
    <Stack gap={2}>
      {items.map((it, i) => (
        <Flex key={i} gap={2} align="flex-start">
          <Box mt="7px" w="6px" h="6px" borderRadius="full" bg={color} flexShrink={0} />
          <Text fontSize="sm">{plain(it)}</Text>
        </Flex>
      ))}
    </Stack>
  );
}

function SourceRow({ src }: { src: ProvisionSource }) {
  return (
    <Flex gap={3} bg="pastinaak" borderRadius="md" px={4} py={3}>
      <Icon
        as={src.verified ? LuShieldCheck : LuShieldAlert}
        color={src.verified ? "#1E9E6A" : "#E8920C"}
        boxSize="16px"
        mt="2px"
        flexShrink={0}
      />
      <Box>
        <Text fontSize="xs" fontWeight="700">
          {src.document_name} — {src.section}{" "}
          <Text as="span" color="fg.muted" fontWeight="400">
            (pagina {src.page_number})
          </Text>
          {src.verified ? (
            <Text as="span" color={src.match_quality === "exact" ? "#1E9E6A" : "#8A5A00"} fontWeight="600">
              {" "}· {src.match_quality === "exact" ? "letterlijk teruggevonden" : "benadering teruggevonden"}
            </Text>
          ) : (
            <Text as="span" color="#B23A2A" fontWeight="600">
              {" "}· niet teruggevonden in bron
            </Text>
          )}
        </Text>
        <Text fontSize="xs" color="fg.muted" fontStyle="italic">
          “{src.quote}”
        </Text>
      </Box>
    </Flex>
  );
}

export function EntitlementCard({ item, index }: { item: EntitlementComparison; index: number }) {
  const [showMore, setShowMore] = useState(false);
  const sev = SEVERITY[item.deviation_severity] ?? SEVERITY.None;
  const allSources = [...item.current_sources, ...item.standard_sources];
  const hasDetail =
    !!plain(item.current_detail) ||
    !!plain(item.standard_detail) ||
    !!item.required_qwik_configuration ||
    allSources.length > 0;

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
          <Flex gap={2} align="center" wrap="wrap">
            {/* Evidence-strength badge — honest trust signal for experts */}
            <Badge
              display="flex"
              alignItems="center"
              gap={1}
              bg={EVIDENCE[item.evidence_level].bg}
              color={EVIDENCE[item.evidence_level].fg}
              borderRadius="full"
              px={3}
              py={1}
              title={
                "Bewijskracht meet hoe goed dit punt is onderbouwd met citaten die in de bron zijn " +
                "teruggevonden (beide kanten, letterlijk vs. benadering). Het zegt niets over of het " +
                "oordeel juist is — dat blijft aan de expert."
              }
            >
              <Icon
                as={item.evidence_level === "Hoog" ? LuShieldCheck : LuShieldAlert}
                boxSize="14px"
              />
              Bewijskracht: {EVIDENCE[item.evidence_level].label} ({item.evidence_score})
            </Badge>
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

        {/* Weak-evidence warning — flag for expert review */}
        {item.evidence_level === "Laag" && (
          <Flex align="center" gap={2} bg="#FEECE8" borderRadius="lg" px={4} py={2} mb={4}>
            <Icon as={LuShieldAlert} color="#B23A2A" boxSize="16px" flexShrink={0} />
            <Text fontSize="sm" color="#8A2A1E">
              Zwakke onderbouwing — dit punt is niet aan beide kanten met een letterlijk citaat
              bevestigd. Controleer het zelf in de bronnen voordat u erop vertrouwt.
            </Text>
          </Flex>
        )}

        {/* Current vs standard — bullets, side by side */}
        <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
          <Box bg="pastinaak" borderRadius="lg" p={4}>
            <Flex align="center" gap={2} mb={3}>
              <Icon as={LuBuilding2} color="marvel.700" boxSize="16px" />
              <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted">
                Huidige regeling van het fonds
              </Text>
            </Flex>
            <BulletList items={item.current_points} color="marvel.600" />
          </Box>
          <Box bg="brand.subtle" borderRadius="lg" p={4}>
            <Flex align="center" gap={2} mb={3}>
              <Icon as={LuPackage} color="marvel.700" boxSize="16px" />
              <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted">
                Standaard Wtp-product
              </Text>
            </Flex>
            <BulletList items={item.standard_points} color="#0E83BF" />
          </Box>
        </SimpleGrid>

        {/* The difference — the thing experts actually want to see */}
        {item.key_differences?.length > 0 && (
          <Box mt={4} bg={sev.bg} borderRadius="lg" p={4}>
            <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted" mb={2}>
              Het verschil
            </Text>
            <Stack gap={2}>
              {item.key_differences.map((d, i) => (
                <Flex key={i} gap={2} align="flex-start">
                  <Icon as={LuTriangleAlert} color={sev.color} boxSize="14px" mt="3px" flexShrink={0} />
                  <Text fontSize="sm" fontWeight="500">
                    {plain(d)}
                  </Text>
                </Flex>
              ))}
            </Stack>
          </Box>
        )}

        {/* What it means — plain language */}
        {plain(item.impact_explanation) && (
          <Box mt={4} borderLeftWidth="3px" borderColor={sev.color} pl={4} py={1}>
            <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted" mb={1}>
              Wat betekent dit?
            </Text>
            <Text fontSize="sm">{plain(item.impact_explanation)}</Text>
          </Box>
        )}

        {/* Collapsible: extra detail + full sources */}
        {hasDetail && (
          <>
            <Flex mt={4}>
              <Button size="xs" variant="ghost" color="marvel.700" onClick={() => setShowMore((s) => !s)}>
                <Icon as={showMore ? LuChevronUp : LuChevronDown} />
                {showMore ? "Minder informatie" : "Meer informatie & onderbouwing"}
              </Button>
            </Flex>

            {showMore && (
              <Stack gap={4} mt={2}>
                {plain(item.current_detail) && (
                  <Box>
                    <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted" mb={1}>
                      Toelichting — huidige regeling
                    </Text>
                    <Text fontSize="sm">{plain(item.current_detail)}</Text>
                  </Box>
                )}
                {plain(item.standard_detail) && (
                  <Box>
                    <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted" mb={1}>
                      Toelichting — standaardproduct
                    </Text>
                    <Text fontSize="sm">{plain(item.standard_detail)}</Text>
                  </Box>
                )}

                {allSources.length > 0 && (
                  <Box>
                    <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted" mb={2}>
                      Bronnen ({allSources.length})
                    </Text>
                    <Stack gap={2}>
                      {item.current_sources.length > 0 && (
                        <Text fontSize="xs" fontWeight="600" color="marvel.700">
                          Fonds
                        </Text>
                      )}
                      {item.current_sources.map((src, i) => (
                        <SourceRow key={`c${i}`} src={src} />
                      ))}
                      {item.standard_sources.length > 0 && (
                        <Text fontSize="xs" fontWeight="600" color="marvel.700" mt={1}>
                          Standaardproduct
                        </Text>
                      )}
                      {item.standard_sources.map((src, i) => (
                        <SourceRow key={`s${i}`} src={src} />
                      ))}
                    </Stack>
                  </Box>
                )}

                {item.required_qwik_configuration && (
                  <Box>
                    <Text fontSize="xs" fontWeight="700" textTransform="uppercase" color="fg.muted" mb={2}>
                      Technische vertaling (Qwik)
                    </Text>
                    <Box
                      as="pre"
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
                  </Box>
                )}
              </Stack>
            )}
          </>
        )}
      </Box>
    </Box>
  );
}
