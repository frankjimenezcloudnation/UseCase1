import { Box, Flex, SimpleGrid, Text } from "@chakra-ui/react";
import type { FundComparisonReport, Severity } from "@/api/analysis";
import { SEVERITY, SEVERITY_ORDER } from "@/lib/severity";

function Tile({
  value,
  label,
  color,
}: {
  value: number | string;
  label: string;
  color: string;
}) {
  return (
    <Box bg="white" borderWidth="1px" borderColor="blackAlpha.200" borderRadius="xl" p={5}>
      <Text fontFamily="heading" fontWeight="700" fontSize="3xl" lineHeight="1" color={color}>
        {value}
      </Text>
      <Text fontSize="sm" color="fg.muted" mt={2}>
        {label}
      </Text>
    </Box>
  );
}

export function SummaryPanel({ report }: { report: FundComparisonReport }) {
  const total = report.entitlements.length;
  const gaps = report.entitlements.filter((e) => e.gap_detected).length;
  const counts = SEVERITY_ORDER.reduce(
    (acc, s) => {
      acc[s] = report.entitlements.filter((e) => e.deviation_severity === s).length;
      return acc;
    },
    {} as Record<Severity, number>,
  );
  const high = counts.High;

  const conclusion =
    high > 0
      ? `Op ${high} van de ${total} onderdelen is er een grote afwijking tussen de fondsregeling en het standaardproduct. Deze vragen om aandacht en maatwerk bij de overgang.`
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
        <Tile value={total} label="Onderzochte onderdelen" color="fg.default" />
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
      >
        <Text fontSize="md" color="fg.default">
          {conclusion}
        </Text>
      </Flex>

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
    </Box>
  );
}
