import { Box, Flex, Icon, SimpleGrid, Stack, Text } from "@chakra-ui/react";
import { LuCircleCheck, LuCircleMinus, LuShieldAlert, LuShieldCheck } from "react-icons/lu";
import { WTP_THEMES, type FundComparisonReport, type Severity } from "@/api/analysis";
import { SEVERITY, SEVERITY_ORDER } from "@/lib/severity";

function Tile({
  value,
  label,
  color,
  hint,
}: {
  value: number | string;
  label: string;
  color: string;
  hint?: string;
}) {
  return (
    <Box bg="white" borderWidth="1px" borderColor="blackAlpha.200" borderRadius="xl" p={5}>
      <Text fontFamily="heading" fontWeight="700" fontSize="3xl" lineHeight="1" color={color}>
        {value}
      </Text>
      <Text fontSize="sm" color="fg.muted" mt={2}>
        {label}
      </Text>
      {hint && (
        <Text fontSize="xs" color="fg.muted" mt={1}>
          {hint}
        </Text>
      )}
    </Box>
  );
}

/** True when any examined area plausibly matches this checklist theme. */
function themeCovered(theme: string, areas: string[]): boolean {
  const keys = theme
    .toLowerCase()
    .split(/[\s/]+/)
    .filter((w) => w.length >= 5); // significant words only
  return areas.some((a) => {
    const la = a.toLowerCase();
    return keys.some((k) => la.includes(k) || k.includes(la.split(/\s+/)[0]));
  });
}

export function SummaryPanel({ report }: { report: FundComparisonReport }) {
  const total = report.entitlements.length;
  const gaps = report.entitlements.filter((e) => e.gap_detected).length;
  const verified = report.entitlements.filter((e) => e.evidence_verified).length;
  const weak = report.entitlements.filter((e) => e.evidence_level === "Laag").length;
  const counts = SEVERITY_ORDER.reduce(
    (acc, s) => {
      acc[s] = report.entitlements.filter((e) => e.deviation_severity === s).length;
      return acc;
    },
    {} as Record<Severity, number>,
  );
  const high = counts.High;
  const areas = report.entitlements.map((e) => e.area);

  const conclusion =
    high > 0
      ? `Op ${high} van de ${total} onderzochte onderdelen is er een grote afwijking tussen de fondsregeling en het standaardproduct. Deze vragen om aandacht en maatwerk bij de overgang.`
      : gaps > 0
        ? `De regeling sluit grotendeels aan, met ${gaps} aandachtspunt${gaps === 1 ? "" : "en"} die een bewuste keuze vragen bij de inrichting.`
        : `De regeling sluit volledig aan op het standaardproduct.`;

  return (
    <Box>
      <Text
        fontFamily="heading"
        fontWeight="700"
        fontSize="xs"
        letterSpacing="0.12em"
        textTransform="uppercase"
        color="marvel.600"
        mb={3}
      >
        Samenvatting
      </Text>

      <SimpleGrid columns={{ base: 2, md: 4 }} gap={4}>
        <Tile
          value={total}
          label="Onderzochte onderdelen"
          color="fg.default"
          hint="Aantal onderwerpen dat de analyse in de documenten kon beoordelen"
        />
        <Tile value={gaps} label="Afwijkingen gevonden" color="#0E83BF" />
        <Tile value={counts.High} label="Grote impact" color="#FE5E3E" />
        <Tile value={counts.Medium} label="Aandachtspunten" color="#E8920C" />
      </SimpleGrid>

      {/* Plain-language conclusion */}
      <Flex
        mt={4}
        bg="brand.subtle"
        borderRadius="xl"
        px={5}
        py={4}
        borderWidth="1px"
        borderColor="marvel.200"
        align="center"
        gap={3}
      >
        <Text fontSize="md" color="fg.default">
          {conclusion}
        </Text>
      </Flex>

      {/* Evidence trust line */}
      <Stack mt={3} gap={1}>
        <Flex align="center" gap={2}>
          <Icon as={LuShieldCheck} color={verified === total ? "#1E9E6A" : "#E8920C"} boxSize="16px" />
          <Text fontSize="sm" color="fg.muted">
            {verified} van de {total} bevindingen zijn aan beide kanten onderbouwd met een citaat dat
            in de bron is teruggevonden.
          </Text>
        </Flex>
        {weak > 0 && (
          <Flex align="center" gap={2}>
            <Icon as={LuShieldAlert} color="#B23A2A" boxSize="16px" />
            <Text fontSize="sm" color="#8A2A1E">
              {weak} bevinding{weak === 1 ? "" : "en"} met zwakke onderbouwing — expert-check
              aanbevolen.
            </Text>
          </Flex>
        )}
      </Stack>

      {/* Severity distribution bar */}
      {gaps > 0 && (
        <Box mt={5}>
          <Flex h="12px" borderRadius="full" overflow="hidden" bg="blackAlpha.100">
            {SEVERITY_ORDER.map((s) =>
              counts[s] > 0 ? (
                <Box
                  key={s}
                  flex={counts[s]}
                  bg={SEVERITY[s].color}
                  title={`${SEVERITY[s].label}: ${counts[s]}`}
                />
              ) : null,
            )}
          </Flex>
          <Flex mt={3} gap={4} wrap="wrap">
            {SEVERITY_ORDER.map((s) => (
              <Flex key={s} align="center" gap={2}>
                <Box w="12px" h="12px" borderRadius="sm" bg={SEVERITY[s].color} />
                <Text fontSize="xs" color="fg.muted">
                  {SEVERITY[s].label} impact · {counts[s]}
                </Text>
              </Flex>
            ))}
          </Flex>
        </Box>
      )}

      {/* Coverage: which WTP themes were examined vs not */}
      <Box
        mt={5}
        borderWidth="1px"
        borderColor="blackAlpha.200"
        borderRadius="xl"
        bg="white"
        p={5}
      >
        <Text fontFamily="heading" fontWeight="700" fontSize="sm" mb={1}>
          Wat is onderzocht?
        </Text>
        <Text fontSize="xs" color="fg.muted" mb={3}>
          Het getal hierboven is niet vast: het is het aantal onderwerpen dat op basis van de
          gekozen documenten daadwerkelijk kon worden beoordeeld. Hieronder ziet u die onderwerpen
          afgezet tegen de standaard WTP-checklist.
        </Text>
        <SimpleGrid columns={{ base: 1, sm: 2 }} gap={2}>
          {WTP_THEMES.map((theme) => {
            const covered = themeCovered(theme, areas);
            return (
              <Flex key={theme} align="center" gap={2}>
                <Icon
                  as={covered ? LuCircleCheck : LuCircleMinus}
                  color={covered ? "#1E9E6A" : "#B9B4AE"}
                  boxSize="16px"
                  flexShrink={0}
                />
                <Text fontSize="sm" color={covered ? "fg.default" : "fg.muted"}>
                  {theme}
                </Text>
              </Flex>
            );
          })}
        </SimpleGrid>
        {areas.some((a) => !WTP_THEMES.some((t) => themeCovered(t, [a]))) && (
          <Text fontSize="xs" color="fg.muted" mt={3}>
            Daarnaast zijn onderwerpen buiten deze checklist onderzocht:{" "}
            {areas.filter((a) => !WTP_THEMES.some((t) => themeCovered(t, [a]))).join(", ")}.
          </Text>
        )}
      </Box>
    </Box>
  );
}
