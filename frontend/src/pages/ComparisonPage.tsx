import { useEffect, useMemo, useState } from "react";
import {
  Badge,
  Box,
  Button,
  Flex,
  Heading,
  Icon,
  SimpleGrid,
  Spinner,
  Stack,
  Text,
} from "@chakra-ui/react";
import {
  LuFileStack,
  LuPlay,
  LuScale,
  LuSparkles,
  LuTriangleAlert,
} from "react-icons/lu";
import {
  analysisApi,
  type AnalysisResponse,
  type DocumentsResponse,
} from "@/api/analysis";
import { DocumentSelector } from "@/components/DocumentSelector";
import { EntitlementCard } from "@/components/EntitlementCard";
import { SummaryPanel } from "@/components/SummaryPanel";

function Step({
  n,
  icon,
  title,
  text,
}: {
  n: number;
  icon: React.ElementType;
  title: string;
  text: string;
}) {
  return (
    <Flex gap={3} align="flex-start">
      <Flex
        align="center"
        justify="center"
        w="40px"
        h="40px"
        borderRadius="xl"
        bg="brand.subtle"
        color="marvel.700"
        flexShrink={0}
      >
        <Icon as={icon} boxSize="20px" />
      </Flex>
      <Box>
        <Text fontFamily="heading" fontWeight="700" fontSize="sm">
          {n}. {title}
        </Text>
        <Text fontSize="sm" color="fg.muted">
          {text}
        </Text>
      </Box>
    </Flex>
  );
}

export function ComparisonPage() {
  const [docs, setDocs] = useState<DocumentsResponse | null>(null);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    analysisApi
      .documents()
      .then((d) => {
        setDocs(d);
        setSelected(new Set([...d.fund, ...d.benchmark].map((x) => x.id)));
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Documenten laden mislukt"));
  }, []);

  const toggle = (id: string) =>
    setSelected((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });

  const fundIds = useMemo(
    () => (docs ? docs.fund.filter((d) => selected.has(d.id)).map((d) => d.id) : []),
    [docs, selected],
  );
  const benchIds = useMemo(
    () => (docs ? docs.benchmark.filter((d) => selected.has(d.id)).map((d) => d.id) : []),
    [docs, selected],
  );

  async function run() {
    setRunning(true);
    setError(null);
    setResult(null);
    try {
      const res = await analysisApi.compare({
        fund_document_ids: fundIds,
        benchmark_document_ids: benchIds,
      });
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Analyse mislukt");
    } finally {
      setRunning(false);
    }
  }

  return (
    <Stack gap={8}>
      {/* Hero */}
      <Box>
        <Text
          fontFamily="heading"
          fontWeight="700"
          fontSize="xs"
          letterSpacing="0.14em"
          textTransform="uppercase"
          color="marvel.600"
        >
          Wet toekomst pensioenen · vergelijking
        </Text>
        <Heading as="h1" fontFamily="heading" fontSize={{ base: "3xl", md: "5xl" }} mt={1} lineHeight="1.1">
          Van fondsregeling naar standaardproduct
        </Heading>
        <Text color="fg.muted" mt={3} fontSize="lg" maxW="3xl">
          Deze verkenner leest de documenten van een pensioenfonds en vergelijkt de
          rechten van deelnemers met het gestandaardiseerde Wtp-product. Zo ziet u in
          één oogopslag <b>waar de regeling afwijkt</b>, hoe groot de impact is, en
          welke onderbouwing daarbij hoort.
        </Text>
      </Box>

      {/* How it works */}
      <SimpleGrid columns={{ base: 1, md: 3 }} gap={5}>
        <Step
          n={1}
          icon={LuFileStack}
          title="Documenten kiezen"
          text="Selecteer de fondsdocumenten en het standaardproduct om mee te vergelijken."
        />
        <Step
          n={2}
          icon={LuScale}
          title="Vergelijken"
          text="De verkenner legt beide naast elkaar en spoort afwijkingen op."
        />
        <Step
          n={3}
          icon={LuSparkles}
          title="Inzicht krijgen"
          text="Bekijk per onderwerp de impact, uitleg en onderbouwing met bronnen."
        />
      </SimpleGrid>

      {error && (
        <Flex align="center" gap={3} bg="#FEECE8" borderRadius="lg" px={4} py={3}>
          <Icon as={LuTriangleAlert} color="#FE5E3E" />
          <Text fontSize="sm">{error}</Text>
        </Flex>
      )}

      {!docs ? (
        <Flex justify="center" py={12}>
          <Spinner color="marvel.400" />
        </Flex>
      ) : (
        <>
          {/* Selection + run */}
          <Box
            borderWidth="1px"
            borderColor="blackAlpha.200"
            borderRadius="2xl"
            bg="white"
            p={{ base: 5, md: 7 }}
            boxShadow="0 1px 2px rgba(0,0,0,.04)"
          >
            <Flex justify="space-between" align="center" mb={5} wrap="wrap" gap={3}>
              <Box>
                <Heading as="h2" fontSize="xl" fontFamily="heading">
                  Stap 1 — Kies de documenten
                </Heading>
                <Text fontSize="sm" color="fg.muted" mt={1}>
                  Standaard staat alles aangevinkt. Vink uit wat u niet wilt meenemen.
                </Text>
              </Box>
              <Badge
                bg={docs.ai_configured ? "mintgroen" : "#D8D4CF"}
                color="black"
                borderRadius="full"
                px={3}
                py={1}
              >
                {docs.ai_configured ? "Live AI-analyse" : "Demovoorbeeld"}
              </Badge>
            </Flex>

            <SimpleGrid columns={{ base: 1, md: 2 }} gap={6}>
              <DocumentSelector
                title="Documenten van het fonds"
                documents={docs.fund}
                selected={selected}
                onToggle={toggle}
              />
              <DocumentSelector
                title="Standaardproduct om mee te vergelijken"
                documents={docs.benchmark}
                selected={selected}
                onToggle={toggle}
              />
            </SimpleGrid>

            <Flex mt={7} gap={4} align="center" wrap="wrap">
              <Button
                size="lg"
                bg="marvel.400"
                color="black"
                fontWeight="700"
                _hover={{ bg: "marvel.500" }}
                _active={{ bg: "marvel.600" }}
                borderRadius="full"
                px={8}
                onClick={run}
                loading={running}
                loadingText="Bezig met vergelijken…"
                disabled={fundIds.length === 0}
              >
                <LuPlay /> Vergelijking starten
              </Button>
              <Text fontSize="sm" color="fg.muted">
                {fundIds.length} fondsdocument{fundIds.length === 1 ? "" : "en"} ·{" "}
                {benchIds.length} standaarddocument{benchIds.length === 1 ? "" : "en"}
              </Text>
            </Flex>
          </Box>

          {/* Loading reassurance */}
          {running && (
            <Flex
              align="center"
              gap={4}
              bg="brand.subtle"
              borderWidth="1px"
              borderColor="marvel.200"
              borderRadius="2xl"
              px={6}
              py={5}
            >
              <Spinner color="marvel.500" />
              <Box>
                <Text fontWeight="700" fontFamily="heading">
                  De documenten worden vergeleken…
                </Text>
                <Text fontSize="sm" color="fg.muted">
                  {docs.ai_configured
                    ? "De regeling wordt gelezen en naast het standaardproduct gelegd. Dit duurt meestal een halve tot een hele minuut."
                    : "Een voorbeeldvergelijking wordt samengesteld."}
                </Text>
              </Box>
            </Flex>
          )}

          {/* Results */}
          {result && !running && (
            <Stack gap={6}>
              <Box>
                <Flex align="baseline" justify="space-between" wrap="wrap" gap={3}>
                  <Box>
                    <Heading as="h2" fontSize="2xl" fontFamily="heading">
                      {result.report.fund_name}
                    </Heading>
                    <Text color="fg.muted" fontSize="sm">
                      Beoogde overgangsdatum: {result.report.target_transition_date}
                    </Text>
                  </Box>
                  <Badge
                    bg={result.mode === "live" ? "marvel.400" : "#D8D4CF"}
                    color="black"
                    borderRadius="full"
                    px={3}
                    py={1}
                  >
                    {result.mode === "live" ? "Live geanalyseerd" : "Demovoorbeeld"}
                  </Badge>
                </Flex>
              </Box>

              <SummaryPanel report={result.report} />

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
                  Bevindingen per onderwerp
                </Text>
                <Stack gap={4}>
                  {result.report.entitlements.map((item, i) => (
                    <EntitlementCard key={i} item={item} index={i} />
                  ))}
                </Stack>
              </Box>
            </Stack>
          )}
        </>
      )}
    </Stack>
  );
}
