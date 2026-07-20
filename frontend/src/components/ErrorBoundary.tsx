import { Component, type ReactNode } from "react";
import { Box, Button, Flex, Heading, Icon, Text } from "@chakra-ui/react";
import { LuTriangleAlert } from "react-icons/lu";

interface Props {
  children: ReactNode;
}
interface State {
  error: Error | null;
}

/**
 * Catches render-time errors anywhere below it and shows a readable fallback
 * instead of unmounting the whole tree (which shows up as a blank white screen).
 * React error boundaries must be class components.
 */
export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: unknown) {
    // Surface the failure in the console for debugging; the UI stays usable.
    console.error("ErrorBoundary caught an error:", error, info);
  }

  render() {
    const { error } = this.state;
    if (!error) return this.props.children;

    return (
      <Box
        borderWidth="1px"
        borderColor="#F3C6BC"
        bg="#FEECE8"
        borderRadius="2xl"
        p={{ base: 5, md: 7 }}
        maxW="3xl"
        mx="auto"
        my={8}
      >
        <Flex align="center" gap={3} mb={3}>
          <Icon as={LuTriangleAlert} color="#B23A2A" boxSize="22px" />
          <Heading as="h2" fontSize="lg" fontFamily="heading" color="#8A2A1E">
            Er ging iets mis bij het tonen van dit scherm
          </Heading>
        </Flex>
        <Text fontSize="sm" color="#8A2A1E" mb={4}>
          De weergave is onverwacht gestopt, maar de applicatie draait nog. Dit gebeurt meestal als de
          gegevens van de server een ander formaat hebben dan verwacht — controleer of de backend de
          nieuwste versie draait en probeer het opnieuw.
        </Text>
        <Box
          as="pre"
          fontFamily="mono"
          fontSize="xs"
          bg="white"
          color="#5B5B60"
          p={3}
          borderRadius="md"
          overflowX="auto"
          whiteSpace="pre-wrap"
          mb={4}
        >
          {error.message}
        </Box>
        <Button
          bg="marvel.400"
          color="black"
          fontWeight="700"
          borderRadius="full"
          px={6}
          _hover={{ bg: "marvel.500" }}
          onClick={() => this.setState({ error: null })}
        >
          Opnieuw proberen
        </Button>
      </Box>
    );
  }
}
