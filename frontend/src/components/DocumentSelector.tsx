import { Box, Flex, Icon, Stack, Text } from "@chakra-ui/react";
import { LuCheck, LuFileText } from "react-icons/lu";
import type { DocumentInfo } from "@/api/analysis";

interface Props {
  title: string;
  documents: DocumentInfo[];
  selected: Set<string>;
  onToggle: (id: string) => void;
}

export function DocumentSelector({ title, documents, selected, onToggle }: Props) {
  return (
    <Box>
      <Text
        fontFamily="heading"
        fontWeight="700"
        fontSize="sm"
        textTransform="uppercase"
        letterSpacing="0.08em"
        color="fg.muted"
        mb={3}
      >
        {title}
      </Text>
      <Stack gap={2}>
        {documents.map((doc) => {
          const isSelected = selected.has(doc.id);
          return (
            <Flex
              key={doc.id}
              align="center"
              gap={3}
              px={4}
              py={3}
              borderWidth="1px"
              borderColor={isSelected ? "marvel.400" : "blackAlpha.200"}
              bg={isSelected ? "brand.subtle" : "white"}
              borderRadius="lg"
              cursor="pointer"
              transition="all 0.15s"
              _hover={{ borderColor: "marvel.400" }}
              onClick={() => onToggle(doc.id)}
            >
              <Flex
                align="center"
                justify="center"
                w="20px"
                h="20px"
                borderRadius="sm"
                borderWidth="2px"
                borderColor={isSelected ? "marvel.400" : "blackAlpha.400"}
                bg={isSelected ? "marvel.400" : "transparent"}
                flexShrink={0}
              >
                {isSelected && <Icon as={LuCheck} color="black" boxSize="14px" />}
              </Flex>
              <Icon as={LuFileText} color="fg.muted" boxSize="18px" flexShrink={0} />
              <Box minW={0}>
                <Text fontWeight="600" fontSize="sm" lineClamp={1}>
                  {doc.doc_type}
                </Text>
                <Text fontSize="xs" color="fg.muted" lineClamp={1}>
                  {doc.filename}
                </Text>
              </Box>
            </Flex>
          );
        })}
      </Stack>
    </Box>
  );
}
