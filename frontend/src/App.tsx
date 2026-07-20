import { Box, Container, Flex, Text } from "@chakra-ui/react";
import { ComparisonPage } from "@/pages/ComparisonPage";
import { ErrorBoundary } from "@/components/ErrorBoundary";

export default function App() {
  return (
    <Box minH="100vh" bg="bg.canvas">
      <Flex
        as="header"
        align="center"
        gap={3}
        px={{ base: 5, md: 10 }}
        py={4}
        bg="black"
        color="white"
      >
        <Box w="10px" h="26px" bg="marvel.400" borderRadius="sm" />
        <Text fontFamily="heading" fontWeight="700" fontSize="lg" letterSpacing="-0.01em">
          CloudNation
        </Text>
        <Text color="whiteAlpha.700" fontSize="sm">
          · WTP Pension Prototyping Engine
        </Text>
      </Flex>

      <Container maxW="5xl" py={{ base: 8, md: 12 }}>
        <ErrorBoundary>
          <ComparisonPage />
        </ErrorBoundary>
      </Container>

      <Box as="footer" textAlign="center" py={8} color="fg.muted" fontSize="xs">
        Enable. Empower. Deliver. — prototype, semantische analyse Wtp-transitie
      </Box>
    </Box>
  );
}
