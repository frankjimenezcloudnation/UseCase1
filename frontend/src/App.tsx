import { Box, Container, Flex, Heading, Spacer } from "@chakra-ui/react";
import { ColorModeButton } from "@/components/ui/color-mode";
import { ItemsPage } from "@/pages/ItemsPage";

export default function App() {
  return (
    <Box minH="100vh">
      <Flex as="header" align="center" px={6} py={4} borderBottomWidth="1px">
        <Heading size="md">UseCase1</Heading>
        <Spacer />
        <ColorModeButton />
      </Flex>

      <Container maxW="3xl" py={10}>
        <ItemsPage />
      </Container>
    </Box>
  );
}
